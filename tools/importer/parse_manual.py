"""Parse the layout appendices of the HWP user manuals (via hwp2md text) into IR.

Used for the Health Screening Cohort, the Senior Cohort, and the Low-Risk Cohort,
whose variable layouts exist only inside the manuals.
"""

from __future__ import annotations

import re

from common import VAR_RE, add_variable, clean, new_period, split_codes

DITTO = "〃"


def tables_in(text: str):
    """Yield (preceding_lines, rows) for each top-level pipe table in hwp2md output."""
    lines = text.splitlines()
    i = 0
    context: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.startswith("<<TABLE"):
            rows = []
            i += 1
            while i < len(lines) and lines[i] != "<<END TABLE>>":
                if lines[i].startswith("|"):
                    rows.append([clean(c) for c in lines[i].strip().strip("|").split(" | ")])
                i += 1
            yield context[-6:], rows
            context = []
        elif line.strip():
            context.append(line.strip())
        i += 1


def split_cell(text: str) -> list[str]:
    return [x.strip() for x in text.split(" / ") if x.strip()]


def layout_rows(rows):
    """Turn a layout table into (var, label, type, lines) tuples, resolving ditto marks."""
    if not rows:
        return []
    head = rows[0]
    try:
        iv = head.index("영문명")
        il = head.index("변수명")
    except ValueError:
        return []
    it = head.index("변수유형") if "변수유형" in head else None
    ir = head.index("비고") if "비고" in head else len(head) - 1
    out = []
    prev_lines: list[str] = []
    for row in rows[1:]:
        if len(row) <= max(iv, il, ir):
            continue
        var = row[iv].replace(" ", "")
        if not VAR_RE.match(var):
            continue
        remark = row[ir]
        lines = prev_lines if remark == DITTO else split_cell(remark)
        prev_lines = lines
        out.append((var, row[il], row[it] if it is not None else "", lines))
    return out


def parse_heals(md_text: str) -> dict:
    sections = [
        ("자격테이블 변수 구성", "jk", "2002-2023"),
        ("명세서(20t) 변수 구성", "gy20", "2002-2023"),
        ("진료내역(30t) 변수 구성", "gy30", "2002-2023"),
        ("상병내역(40t) 변수 구성", "gy40", "2002-2023"),
        ("처방전교부상세내역(60t) 변수 구성", "gy60", "2002-2023"),
        ("일반건강검진(2002~2008년)", "gj", "2002-2008"),
        ("일반건강검진(2009~2017년)", "gj", "2009-2017"),
        ("일반건강검진(2018~2023년)", "gj", "2018-2023"),
        ("생애전환기건강진단(2007~2017년)", "lj", "2007-2017"),
        ("구강검진(일반)(2002~2008년)", "go", "2002-2008"),
        ("구강검진(일반)(2009~2015년)", "go", "2009-2015"),
        ("구강검진(생애)(2007~2008년)", "lo", "2007-2008"),
        ("구강검진(생애)(2009~2015년)", "lo", "2009-2015"),
        ("구강검진(일반+생애)(2014~2023년)", "go2", "2014-2023"),
        ("요양기관테이블 구성", "yk", "2002-2023"),
    ]
    titles = {
        "jk": "자격 DB", "gy20": "진료 DB 명세서(20t)", "gy30": "진료 DB 진료내역(30t)",
        "gy40": "진료 DB 상병내역(40t)", "gy60": "진료 DB 처방전교부상세내역(60t)",
        "gj": "일반건강검진", "lj": "생애전환기건강진단", "go": "구강검진(일반)",
        "lo": "구강검진(생애)", "go2": "구강검진(일반+생애 통합)", "yk": "요양기관 DB",
    }
    return parse_appendix(md_text, "heals", sections, titles, start_marker="【별첨 1】",
                          codes_marker="【별첨 2】")


def parse_senior(md_text: str) -> dict:
    sections = [
        ("자격테이블 변수 구성", "jk", "2002-2023"),
        ("명세서(20t) 변수 구성", "gy20", "2002-2023"),
        ("진료내역(30t) 변수 구성", "gy30", "2002-2023"),
        ("상병내역(40t) 변수 구성", "gy40", "2002-2023"),
        ("처방전교부상세내역(60t) 변수 구성", "gy60", "2002-2023"),
        ("일반건강검진 및 생애전환기건강진단(2002~2017년)", "gj", "2002-2017"),
        ("일반건강검진(2018~2023년)", "gj", "2018-2023"),
        ("요양기관", "yk", "2002-2023"),
        ("장기요양 신청 및 등급, 인정조사 결과(T01)", "t01", "2008-2023"),
        ("인정조사사항(T02)", "t02", "2008-2023"),
        ("청구명세서(T04)", "t04", "2008-2023"),
        ("장기요양시설 현황(T05)", "t05", "2008-2023"),
    ]
    titles = {
        "jk": "자격 DB", "gy20": "진료 DB 명세서(20t)", "gy30": "진료 DB 진료내역(30t)",
        "gy40": "진료 DB 상병내역(40t)", "gy60": "진료 DB 처방전교부상세내역(60t)",
        "gj": "일반건강검진 및 생애전환기건강진단", "yk": "요양기관 DB",
        "t01": "장기요양 신청 및 판정결과(T01)", "t02": "인정조사사항(T02)",
        "t04": "청구명세서(T04)", "t05": "장기요양시설 현황(T05)",
    }
    return parse_appendix(md_text, "senior", sections, titles,
                          start_marker="■ 노인코호트DB 연도별 레이아웃",
                          codes_marker="■ 노인코호트DB 코드표")


def parse_appendix(md_text, ds_id, sections, titles, start_marker, codes_marker) -> dict:
    start = md_text.index(start_marker)
    end = md_text.index(codes_marker, start)
    body, codes_text = md_text[start:end], md_text[end:]
    tables = {}
    order = []
    for context, rows in tables_in(body):
        joined = " ".join(context)
        hit = None
        for key, tid, years in sections:
            if key in joined:
                hit = (tid, years)
        if not hit:
            # The first table after the start marker is the eligibility table.
            if not order and rows and rows[0][:2] == ["연번", "변수명"]:
                hit = ("jk", "2002-2023")
            else:
                continue
        tid, years = hit
        if tid not in tables:
            tables[tid] = {"id": tid, "title_ko": titles[tid], "variables": []}
            order.append(tid)
        for var, label, type_, lines in layout_rows(rows):
            add_variable(tables[tid], var, new_period(years, label, type_, lines))
    return {"id": ds_id, "tables": [tables[t] for t in order],
            "code_lists": parse_code_appendix(codes_text)}


def parse_code_appendix(text: str) -> dict:
    lists = {}
    for context, rows in tables_in(text):
        if not rows or "코드" not in rows[0]:
            continue
        head = rows[0]
        iv, ic = head.index("영문명"), head.index("코드")
        for row in rows[1:]:
            if len(row) <= max(iv, ic):
                continue
            names = [n.strip() for n in row[iv].replace(" / ", ",").split(",") if n.strip()]
            codes, notes = [], []
            for line in split_cell(row[ic]):
                if line.startswith(("※", "(", "…", "[")):
                    notes.append(line.lstrip("※ "))
                    continue
                found = split_codes(line)
                codes.extend(found)
            for n in names:
                if VAR_RE.match(n):
                    lists[n] = codes + [{"note_ko": x} for x in notes]
        break
    return lists


def parse_lowrisk(md_text: str) -> dict:
    tables = {"SMPL_MC": {"id": "smpl_mc", "title_ko": "SMPL_MC (의료이용)", "variables": []},
              "SMPL_HC": {"id": "smpl_hc", "title_ko": "SMPL_HC (건강검진)", "variables": []}}
    for context, rows in tables_in(md_text):
        if not rows or rows[0][:3] != ["테이블명", "연번", "변수명"]:
            continue
        current = None
        for row in rows[1:]:
            name = row[0].split(" / ")[0].strip()
            if name in tables:
                current = tables[name]
            if not current or len(row) < 4:
                continue
            var, desc = row[2], row[3]
            parts = [p.strip() for p in desc.replace(" / ", "  ").split("  ※") ]
            label = parts[0].strip()
            lines = []
            for p in parts[1:]:
                for seg in re.split(r"\s{2,}| / ", p):
                    if seg.strip():
                        lines.append(seg.strip())
            years = "2014-2023"
            add_variable(current, var, new_period(years, label, "", lines))
        break
    return {"id": "lowrisk", "tables": list(tables.values()), "code_lists": {}}
