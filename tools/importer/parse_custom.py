"""Parse the customized research DB (맞춤형연구DB) layout workbooks into IR."""

from __future__ import annotations

import pathlib
import re

from common import (VAR_RE, add_variable, clean, classify_lines, dedupe, new_period,
                    norm_years, read_sheet, split_codes)

YEARS_RE = re.compile(r"^\d{4}(?:\s*[~\-]\s*\d{4})?$")


def parse(src: pathlib.Path) -> dict:
    tables: list[dict] = []

    def table(tid, title_ko, source, group=None):
        t = {"id": tid, "title_ko": title_ko, "source": source, "variables": []}
        if group:
            t["group"] = group
        tables.append(t)
        return t

    base = src / "맞춤형 자료 제공 컬럼 레이아웃_260910.xlsx"
    names = {
        "자격 및 보험료 (BFC)": ("bfc", "자격 및 보험료 (BFC)"),
        "사망자료 (DTH)": ("dth", "사망자료 (DTH)"),
        "청구명세서 (T20)": ("t20", "청구명세서 (T20)"),
        "진료내역 (T30)": ("t30", "진료내역 (T30)"),
        "상병내역 (T40)": ("t40", "상병내역 (T40)"),
        "처방상세내역 (T60)": ("t60", "처방전교부상세내역 (T60)"),
    }
    long_tables(base, "맞춤형 제공 컬럼", names, table, "basic", base.name)

    # Screening target table, documented only in the 2026 application form.
    t = table("g1e_obj", "일반1차검진 대상자 (G1E_OBJ)", "customized_DB_application_2026.xlsx", "basic")
    for name, label in (("EXMD_BZ_YYYY", "검진사업년도"), ("INDI_DSCM_NO", "개인식별ID"),
                        ("WKG_TYPE_CD", "근무구분코드")):
        add_variable(t, name, new_period("2002-2024", label))

    general = src / "일반건강검진 자료 제공 컬럼 레이아웃_260910.xlsx"
    gq = table("gq_rst", "일반1차검진 문진 (GQ_RST)", general.name, "basic")
    gr = table("g1e_rst", "일반1차검진 결과 (G1E_RST)", general.name, "basic")
    for sheet in ("2002-2008", "2009-2017", "2018", "2019-2025"):
        block_sheet(general, sheet, {"문진": gq, "검진": gr}, default=gr)

    inst = src / "요양기관 자료 제공 컬럼 레이아웃_260910.xlsx"
    long_tables(inst, "요양기관", {"요양기관(INST)": ("inst", "요양기관 (INST)")}, table,
                "additional", inst.name)

    ltc = src / "장기요양 자료 제공 컬럼 레이아웃_260910.xlsx"
    long_tables(ltc, "장기요양 테이블", {
        "인정조사": ("ltc_rcgt", "장기요양 신청 및 등급, 인정조사"),
        "욕구조사": ("ltc_need", "장기요양 욕구조사"),
        "청구내역": ("ltc_clm", "장기요양 청구내역"),
        "인력 및 기관": ("ltc_inst", "장기요양 인력 및 기관"),
    }, table, "additional", ltc.name)

    cancer = src / "암 검진 자료 제공 컬럼 레이아웃_260910.xlsx"
    for sheet, tid in (("위암검진", "cst"), ("간암검진", "clv"), ("대장암검진", "ccr"),
                       ("유방암검진", "cbr"), ("자궁경부암검진", "ccx"), ("폐암검진", "clu")):
        t = table(tid, sheet, cancer.name, "additional")
        block_sheet(cancer, sheet, {}, default=t)

    cq_path = src / "암 문진 자료 제공 컬럼 레이아웃_260910.xlsx"
    cq = table("cq", "암검진 문진", cq_path.name, "additional")
    for sheet in ("2002_2005", "2006", "2007_2008", "2009_2018", "2019_2025"):
        block_sheet(cq_path, sheet, {}, default=cq)

    infant = src / "영유아건강검진 자료 제공 컬럼 레이아웃_260910.xlsx"
    t = table("inf_tgt", "영유아건강검진 대상자", infant.name, "additional")
    block_sheet(infant, "대상자", {}, default=t)
    for k in range(8):
        t = table(f"inf{k}", f"영유아건강검진 {k}차", infant.name, "additional")
        block_sheet(infant, f"{k}차", {}, default=t)

    t = table("mother_child", "산모-신생아 자료", "customized_DB_application_2026.xlsx", "additional")
    add_variable(t, "MOTHER_ID", new_period("2002-2024", "개인식별ID(산모)"))
    add_variable(t, "CHID_ID", new_period("2002-2024", "개인식별ID(신생아)"))

    for t in tables:
        t["variables"] = [v for v in t["variables"] if v["periods"]]
    return {"id": "custom", "tables": [t for t in tables if t["variables"]],
            "code_lists": {"INDTP_CD": industry_codes(base)}}


def long_tables(path, sheet, names, table, group, source):
    """Long layout: table, count, number, variable, label, then code/label pairs, then a remark."""
    rows = read_sheet(path, sheet, fill_merged=False)
    filled = read_sheet(path, sheet, fill_merged=True)
    current = None
    var = label = None
    lines: list[str] = []
    codes: list[dict] = []
    created = {}

    def flush():
        if current and var:
            p = new_period(years_for(current["id"]), label, "", lines, codes)
            add_variable(current, var, p)

    for raw, row in zip(rows, filled):
        tname = row[0]
        if tname in names:
            tid, title = names[tname]
            if tid not in created:
                created[tid] = table(tid, title, source, group)
            if created[tid] is not current:
                flush()
                var = None
                current = created[tid]
        if not current:
            continue
        name = raw[3]
        detail = raw[5:15]
        remark = raw[15] if len(raw) > 15 else ""
        if VAR_RE.match(name or ""):
            flush()
            var, label, lines, codes = name, raw[4], [], []
        elif not var:
            continue
        cells = [c for c in detail]
        nonempty = [c for c in cells if c]
        if not nonempty:
            pass
        elif len(nonempty) == 1 and cells[0]:
            lines.append(cells[0])
        else:
            start = 0
            if cells[0] and cells[0].startswith("명세서항코드"):
                group_ko = cells[0]
                start = 2
            else:
                group_ko = None
            for i in range(start, len(cells) - 1, 2):
                code, lab = cells[i], cells[i + 1]
                if code and lab:
                    c = {"code": code, "label_ko": lab}
                    if group_ko:
                        c["group_ko"] = group_ko
                    codes.append(c)
        if remark:
            lines.append("※ " + remark)
    flush()


def years_for(tid: str) -> str:
    if tid.startswith("ltc"):
        return "2008-2024"
    return "2002-2024"


def block_sheet(path, sheet, sections: dict, default):
    """Wide layout with one block of columns per period."""
    rows = read_sheet(path, sheet, fill_merged=True)
    raw_rows = read_sheet(path, sheet, fill_merged=False)
    # Find the row with period labels.
    prow = None
    for i, row in enumerate(rows[:6]):
        starts = [j for j, c in enumerate(raw_rows[i]) if YEARS_RE.match(c or "")]
        if starts:
            prow = i
            break
    if prow is None:
        raise ValueError(f"{path.name}:{sheet}: no period header")
    starts = [j for j, c in enumerate(raw_rows[prow]) if YEARS_RE.match(c or "")]
    periods = [(j, norm_years(raw_rows[prow][j])) for j in starts]
    width = starts[1] - starts[0] if len(starts) > 1 else None
    # Header row just below the periods tells which kind of block this is. Read it
    # unfilled, because merged header cells would otherwise repeat their labels.
    header = raw_rows[prow + 1] if prow + 1 < len(raw_rows) else []
    kind = "A"  # column, then values; the Korean label sits in a shared column
    if width is None:
        width = 7 if not any("변수" in (c or "") for c in header) else len(header) - starts[0]
    sub = [header[starts[0] + k] if starts[0] + k < len(header) else "" for k in range(width)]
    if len(sub) > 1 and sub[1].replace(" ", "") == "변수명":
        kind = "B2" if width == 2 else "B"  # column, label, value
    target = default
    groups: dict[tuple, dict] = {}
    order: list[tuple] = []
    for r in range(prow + 1, len(rows)):
        row, raw = rows[r], raw_rows[r]
        first = row[0] if row else ""
        if first.startswith("**"):
            sec = first.strip("* ").strip()
            for key, t in sections.items():
                if key in sec:
                    target = t
            continue
        if first in ("순번",) or (row[1] if len(row) > 1 else "") in ("컬럼 명", "컬럼명"):
            continue
        shared_label = row[1] if len(row) > 1 else ""
        for start, years in periods:
            cells = row[start:start + width]
            if not cells or not VAR_RE.match(cells[0] or ""):
                continue
            col = cells[0]
            if kind == "A":
                label = shared_label
                vals = cells[1:]
            else:
                label = cells[1] if len(cells) > 1 else ""
                vals = cells[2:] if kind == "B" else []
            key = (id(target), col, years, label)
            if key not in groups:
                groups[key] = {"table": target, "col": col, "years": years, "label": label,
                               "lines": [], "codes": []}
                order.append(key)
            g = groups[key]
            parse_values(vals, g)
    for key in order:
        g = groups[key]
        p = new_period(g["years"], g["label"], "", g["lines"], g["codes"])
        add_variable(g["table"], g["col"], p)


def parse_values(vals: list[str], g: dict) -> None:
    vals = [v for v in vals]
    nonempty = [v for v in vals if v and v != "-"]
    if not nonempty:
        return
    if len(set(nonempty)) == 1 and (len(nonempty) == len([v for v in vals if v]) ):
        text = nonempty[0]
        found = split_codes(text) or loose_codes(text)
        if found:
            g["codes"].extend(found)
        else:
            g["lines"].append(text)
        return
    # Code/label pairs laid out across cells.
    for i in range(0, len(vals) - 1, 2):
        code, lab = vals[i], vals[i + 1]
        if code and lab and code != lab:
            g["codes"].append({"code": code, "label_ko": lab})
        elif code and not lab:
            found = split_codes(code) or loose_codes(code)
            if found:
                g["codes"].extend(found)
            else:
                g["lines"].append(code)


def loose_codes(text: str) -> list[dict]:
    """Codes written without colons, such as '1정상; 2질환의심' or '1:예;2:아니오;'."""
    parts = [p.strip() for p in re.split(r"[;,]", text) if p.strip()]
    out = []
    for p in parts:
        m = re.match(r"^([0-9]{1,2})\s*[:.]?\s*([^\d].*)$", p)
        if not m:
            return []
        out.append({"code": m.group(1), "label_ko": m.group(2).strip()})
    return out if len(out) >= 2 else []


def industry_codes(path) -> list[dict]:
    rows = read_sheet(path, "사업장업종세분류", fill_merged=False)
    out = []
    for row in rows:
        for i in range(0, len(row) - 1, 2):
            code, lab = row[i], row[i + 1]
            if re.fullmatch(r"\d{6}", code or "") and lab:
                out.append({"code": code, "label_ko": lab})
    return sorted(out, key=lambda c: c["code"])
