"""Parse the National Sample Cohort layout workbook (표본코호트DB 레이아웃.xlsx) into IR."""

from __future__ import annotations

import re

from common import VAR_RE, add_variable, clean, new_period, read_sheet, split_codes

# Section headings in the workbook mapped to table ids and years.
SECTIONS = [
    (r"^2-1\.", "bnc", "2002-2023"),
    (r"^2-2\.", "bnd", "2002-2023"),
    (r"^3-1\.", "t20", "2002-2023"),
    (r"^3-2\.", "t30", "2002-2023"),
    (r"^3-3\.", "t40", "2002-2023"),
    (r"^3-4\.", "t60", "2002-2023"),
    (r"^4-1\.", "g1e", "2002-2008"),
    (r"^4-2\.", "g1e", "2009-2017"),
    (r"^4-3\.", "g1e", "2018-2023"),
    (r"^5\. 요양기관", "inst", "2002-2023"),
    (r"^6-1\.", "t01", "2008-2023"),
    (r"^6-2\.", "t02", "2008-2023"),
    (r"^6-3\.", "t04", "2008-2023"),
    (r"^6-4\.", "t05", "2008-2023"),
]

TABLES = {
    "bnc": "자격 및 보험료 테이블",
    "bnd": "출생 및 사망 테이블",
    "t20": "진료 테이블 명세서(T20)",
    "t30": "진료 테이블 진료내역(T30)",
    "t40": "진료 테이블 상병내역(T40)",
    "t60": "진료 테이블 처방전교부상세내역(T60)",
    "g1e": "건강검진 테이블",
    "inst": "요양기관 테이블",
    "t01": "장기요양 신청 및 판정결과(T01)",
    "t02": "장기요양 인정조사사항(T02)",
    "t04": "장기요양 청구명세서(T04)",
    "t05": "장기요양기관 현황(T05)",
}

# Variables whose codes live in the code-list sheet (7.코드표).
CODE_REFS = {
    "FORM_CD": "FORM_CD",
    "MCARE_SUBJ_CD": "SUBJ_CD",
    "DISP_SUBJ_TYPE": "DISP_SUBJ_CD",
    "OFIJ_TYPE": "OFIJ_TYPE",
    "CLA_CD": "CLA_CD",
    "ITEM_CD": "ITEM_CD",
    "CLSF_PTTN_CD": "CLSF_PTTN_CD",
    "INST_CLSFC_CD": "INST_CLSFC_CD",
    "SGG": "SGG",
    "SGG_INST": "SGG",
    "SPCF_SYM_TYPE": "SPCF_SYM_TYPE",
    "G1E_CHST_XRAY_RST": "G1E_CHST_XRAY_RST",
    "DETAIL_TMSG_SUBJ_CD": "DETAIL_TMSG_SUBJ_CD",
}


def parse(path) -> dict:
    ds = {
        "id": "nsc",
        "tables": [{"id": t, "title_ko": title, "variables": []} for t, title in TABLES.items()],
        "code_lists": parse_code_lists(path),
    }
    tables = {t["id"]: t for t in ds["tables"]}
    sheets = ["2.자격 및 보험료 레이아웃", "3.진료 레이아웃", "4.건강검진 레이아웃",
              "5.요양기관_레이아웃", "6.장기요양"]
    for sheet in sheets:
        rows = read_sheet(path, sheet)
        current, years, cols = None, None, None
        group = None  # (number, var, label, type, lines)

        def flush():
            nonlocal group
            if group and current:
                num, var, label, type_, lines = group
                period = new_period(years, label, type_, lines)
                if var in CODE_REFS and not period["codes"]:
                    period["code_ref"] = CODE_REFS[var]
                add_variable(tables[current], var, period)
            group = None

        for row in rows:
            first = row[0]
            hit = next(((t, y) for pat, t, y in SECTIONS if re.match(pat, first)), None)
            if hit:
                flush()
                current, years = hit
                cols = None
                continue
            if first == "연번":
                cols = header_columns(row)
                continue
            if not cols or not current:
                continue
            var = row[cols["var"]] if cols["var"] < len(row) else ""
            if not VAR_RE.match(var):
                # A continuation line whose variable cell is empty belongs to the open group.
                if group and any(row):
                    group[4].append(row[cols["value"]])
                continue
            label = row[cols["label"]]
            type_ = " ".join(x for x in (row[cols["type"]], row[cols["len"]]) if x)
            value = row[cols["value"]] if cols["value"] < len(row) else ""
            key = (first, var)
            if group and (group[0], group[1]) == key:
                group[4].append(value)
                if label and label not in group[2]:
                    # Labels split across rows, as in the 2018-2023 screening layout.
                    group[2] = f"{group[2]} {label}"
            else:
                flush()
                group = [first, var, label, type_, [value]]
        flush()
    return ds


def header_columns(row: list[str]) -> dict:
    """Locate columns in a header row; the screening sheet puts the Korean label first."""
    idx = {name: i for i, name in enumerate(row) if name}
    if "영문명" in idx:  # screening layout: 연번, 변수명(Korean), 영문명(variable), 유형, 길이, 비고
        return {"var": idx["영문명"], "label": idx["변수명"], "type": idx["유형"],
                "len": idx["길이"], "value": idx["비고"]}
    return {"var": idx["변수명"], "label": idx["변수 설명"], "value": idx["변수값 설명"],
            "type": idx.get("형식", idx.get("길이")), "len": idx.get("길이", idx.get("형식"))}


def parse_code_lists(path) -> dict:
    """Read the 7.코드표 sheet into named code lists."""
    rows = read_sheet(path, "7.코드표")
    lists: dict[str, list] = {}
    names = {
        "1": "FORM_CD", "2": "SUBJ_CD", "3": "OFIJ_TYPE", "4": "CLA_CD", "5": "ITEM_CD",
        "6": "CLSF_PTTN_CD", "7": "INST_CLSFC_CD", "9": "SPCF_SYM_TYPE",
        "10": "G1E_CHST_XRAY_RST", "11": "DISP_SUBJ_CD", "12": "DETAIL_TMSG_SUBJ_CD",
    }
    sido = {}
    for row in rows:
        num = row[0]
        if num == "8" or (num == "" and len(row) > 2 and re.fullmatch(r"\d{2}", row[1] or "")):
            # District list: 시도코드 rows give provinces, later rows give districts.
            if row[1] in ("SGG, SGG_INST", "시도코드"):
                c = split_codes(row[3])
                for x in c:
                    sido[x["code"]] = x["label_ko"]
                continue
            if re.fullmatch(r"\d{5}", row[2] or ""):
                lists.setdefault("SGG", []).append(
                    {"code": row[2], "label_ko": f"{row[3]} {row[4]}".strip()})
            continue
        name = names.get(num)
        if not name:
            continue
        lst = lists.setdefault(name, [])
        if name == "ITEM_CD":
            parent = row[3]
            for c in split_codes(row[4]):
                c["group_ko"] = parent
                lst.append(c)
            continue
        if num in ("9", "10", "11", "12"):
            code, label = row[3], row[4]
            if code in ("코드", "") or not label:
                if label and not code:
                    lst.append({"note_ko": label})
                continue
            lst.append({"code": code, "label_ko": label})
            continue
        line = row[3]
        if line.startswith("※") or line.startswith("("):
            lst.append({"note_ko": line.lstrip("※ ").strip()})
            continue
        found = split_codes(line)
        if not found and line.startswith("-"):
            found = [{"code": "-", "label_ko": line.lstrip("- ").strip()}]
        lst.extend(found)
    lists["SIDO"] = [{"code": k, "label_ko": v} for k, v in sido.items()]
    return lists
