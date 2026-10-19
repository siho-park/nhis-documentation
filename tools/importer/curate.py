"""Corrections applied to the IR before it becomes codebook YAML.

The NHIS layout files and manuals are written for people reading a printed
table, so some cells do not survive a mechanical import. This module fixes the
known cases and records each fix as an English note on the variable, so a
reader can see where the codebook departs from the source.

Each rule names the dataset and table it applies to. Generic rules (year
markers, duplicate codes) run on every dataset.
"""

from __future__ import annotations

import copy
import re

from common import merge_years, same_content


_tr = str  # translator for Korean labels quoted inside English notes; set by curate()


def curate(ds_id: str, ir: dict, tr=str) -> None:
    global _tr
    _tr = tr
    for t in ir["tables"]:
        for v in t["variables"]:
            v.setdefault("notes_en", [])
            for p in v["periods"]:
                p.setdefault("notes_en", [])
    tables = {t["id"]: t for t in ir["tables"]}

    admission_route(ds_id, tables)
    if ds_id == "nsc":
        nsc_screening_2018(tables["g1e"])
        nsc_past_history(tables["g1e"])
        nsc_family_history(tables["g1e"])
        blank_label(tables["t02"], "STD_YYYYMM", "기준년월", "T05")
    if ds_id == "custom":
        drop_codes(tables["gq_rst"], "Q_SMK_YN", "금연시작연도")
        drop_codes(tables["gq_rst"], "Q_SMK_DRT", "흡연시작연도")

    for t in ir["tables"]:
        for v in t["variables"]:
            v["periods"] = [q for p in v["periods"] for q in split_since_2009(p)]
            v["periods"] = [q for p in v["periods"] for q in split_by_year_marks(p)]
            merge_periods(v)
            flag_duplicate_codes(v)


# --- Specific rules ---------------------------------------------------------

ROUTE_CODES = [  # As listed in the customized DB layout (2026), which spells out the pairs.
    ("11", "타요양기관경유하여 응급실"), ("12", "타요양기관경우하여 외래"),
    ("21", "응급구조대 후송으로 응급실"), ("22", "응급구조대 후송으로 외래"),
    ("31", "기타 경로로 응급실"), ("32", "기타 경로로 외래"),
]


def admission_route(ds_id: str, tables: dict) -> None:
    """The cohort manuals list each digit of the admission route separately."""
    where = {"nsc": ("t20", "HSPTZ_PATH_TYPE"), "heals": ("gy20", "IN_PAT_CORS_TYPE"),
             "senior": ("gy20", "IN_PAT_CORS_TYPE")}.get(ds_id)
    if not where:
        return
    v = find(tables[where[0]], where[1])
    for p in v["periods"]:
        extra = [c for c in p["codes"] if not c["code"].isdigit()]
        p["codes"] = [{"code": c, "label_ko": label} for c, label in ROUTE_CODES] + extra
    v["notes_en"].append(
        "The source lists the two digits separately, with the first digit giving the arrival "
        "route (1 via another provider, 2 by ambulance, 3 other) and the second digit giving "
        "the admission route (1 emergency room, 2 outpatient department). The combined codes "
        "and their labels are taken from the customized DB layout of 2026."
    )


def nsc_screening_2018(t: dict) -> None:
    """In the 2018-2023 layout, one description cell serves a group of adjacent rows."""
    groups = [
        (["G1E_VA_LT", "G1E_VA_RT"], ["0.1~2.0"], [], [("9.9", "실명")]),
        (["G1E_HA_LT", "G1E_HA_RT"], [], [], [("1", "정상"), ("2", "비정상")]),
        (["G1E_BP_SYS", "G1E_BP_DIA"], ["mmHg"], [], []),
        (["G1E_FBS", "G1E_TOT_CHOL", "G1E_TG", "G1E_HDL", "G1E_LDL", "G1E_CRTN"],
         ["mg/dL"], ["0값 결측처리"], []),
        (["G1E_SGOT", "G1E_SGPT", "G1E_GGT"], ["U/L"], ["0값 결측처리"], []),
        (["Q_PHX_TX_ETC"], [], [], [("0", "미해당"), ("1", "해당")]),
    ]
    note = ("In the 2018 to 2023 layout, one description cell spans this group of rows "
            "({}), and the description above applies to each of them.")
    for names, desc, notes, codes in groups:
        for name in names:
            p = period(find(t, name), "2018-2023")
            p["desc_ko"], p["notes_ko"] = list(desc), list(notes)
            p["codes"] = [{"code": c, "label_ko": label} for c, label in codes]
            if len(names) > 1:
                p["notes_en"].append(note.format(", ".join(names)))


def nsc_past_history(t: dict) -> None:
    """The 2002-2008 past-history codes sit in one shared note instead of each row."""
    diseases = [("1", "결핵"), ("2", "간염"), ("3", "간장질환"), ("4", "고혈압"), ("5", "심장병"),
                ("6", "뇌졸중"), ("7", "당뇨병"), ("8", "암"), ("9", "기타질환")]
    for k in "123":
        for name, codes, desc in [
            (f"Q_PHX{k}_DZ_V0208", diseases, []),
            (f"Q_PHX{k}_YR", [], ["YYYY"]),
            (f"Q_PHX{k}_CR", [("1", "완치"), ("2", "치료중")], []),
        ]:
            p = period(find(t, name), "2002-2008")
            p["codes"] = [{"code": c, "label_ko": label} for c, label in codes]
            p["desc_ko"], p["notes_ko"] = desc, []
            p["notes_en"].append(
                "Up to three past conditions are recorded, each with its code "
                f"(Q_PHXn_DZ_V0208), year of onset (Q_PHXn_YR), and cure status (Q_PHXn_CR).")
    v = find(t, "Q_AWR_DZ")
    for p in v["periods"]:
        p["codes"] = []
    v["notes_en"].append("A free-text field. The layout repeats the codes of Q_AWR_YN in this "
                         "row, and they are omitted here because they do not apply to text.")


def nsc_family_history(t: dict) -> None:
    """Sources disagree on the 2018-2023 coding of family history."""
    for name in ["Q_FHX_HTN", "Q_FHX_STK", "Q_FHX_HTDZ", "Q_FHX_DM", "Q_FHX_ETC"]:
        v = find(t, name)
        out = []
        for p in v["periods"]:
            if "2018" not in p["years"]:
                out.append(p)
                continue
            if p["years"] != "2018-2023":
                early = copy.deepcopy(p)
                early["years"] = p["years"].split(",")[0].strip()
                out.append(early)
            late = copy.deepcopy(p)
            late["years"] = "2018-2023"
            late["codes"] = [{"code": "0", "label_ko": "미해당"}, {"code": "1", "label_ko": "해당"}]
            out.append(late)
        v["periods"] = out
        v["status"] = "disputed"
        v["notes_en"].append(
            "Sources disagree on the coding for 2018 to 2023. The NSC layout file and the "
            "layout table in the NSC manual list 1 none and 2 present, while the manual text "
            "states that 0 not applicable and 1 applicable are used from 2009 to 2023, and the "
            "customized DB layout lists 0 no and 1 yes from 2018. The codes shown follow the "
            "manual text, so check the values in your extract before coding this variable."
        )


def blank_label(t: dict, name: str, label: str, other: str) -> None:
    """Fill a label the layout leaves blank with the label of the same variable elsewhere."""
    v = find(t, name)
    for p in v["periods"]:
        p["label_ko"] = p["label_ko"] or label
    v["notes_en"].append(f"The layout leaves the label of this variable blank, and the label shown "
                         f"is the one given for the same variable in {other}.")


def drop_codes(t: dict, name: str, label: str) -> None:
    """Remove a code whose label is the name of a neighbouring variable."""
    v = find(t, name)
    for p in v["periods"]:
        p["codes"] = [c for c in p["codes"] if c["label_ko"] != label]


# --- Generic rules ----------------------------------------------------------

YEAR_MARKS = [
    (re.compile(r"^~\s*(\d{4})년?( 문진항목)?$"), lambda m, lo, hi: (lo, int(m[1]))),
    (re.compile(r"^(\d{4})년?( 문진항목)?$"), lambda m, lo, hi: (int(m[1]), int(m[1]))),
    (re.compile(r"^(\d{4})년?\s*~$"), lambda m, lo, hi: (int(m[1]), hi)),
    (re.compile(r"^(\d{4})년?부터 적용$"), lambda m, lo, hi: (int(m[1]), hi)),
    (re.compile(r"^(\d{4})\s*~\s*(\d{4})년?$"), lambda m, lo, hi: (int(m[1]), int(m[2]))),
]
TRAILING_MARK = re.compile(r"\s*※\s*(\d{4})년$")


def bounds(years: str):
    found = re.findall(r"\d{4}", years)
    if not found or "," in years:
        return None
    return int(found[0]), int(found[-1])


def fmt(lo: int, hi: int) -> str:
    return str(lo) if lo == hi else f"{lo}-{hi}"


def code_runs(codes: list[dict]) -> list[list[dict]]:
    """Split a code list where numbering restarts, which marks a second code set."""
    runs: list[list[dict]] = []
    prev = None
    for c in codes:
        key = (0, float(c["code"])) if re.fullmatch(r"\d+(\.\d+)?", c["code"]) else (1, c["code"])
        if prev is None or key <= prev:
            runs.append([])
        runs[-1].append(c)
        prev = key
    return runs


def split_by_year_marks(p: dict) -> list[dict]:
    """Apply notes such as '※ 2018년' or '2019부터 적용' to the years of a period."""
    span = bounds(p["years"])
    if not span:
        return [p]
    marks, keep = [], []
    for n in p["notes_ko"]:
        m = next(((rx, f) for rx, f in YEAR_MARKS if rx.match(n)), None)
        if m:
            marks.append(m[1](m[0].match(n), *span))
        else:
            keep.append(n)
    desc = []
    for d in p["desc_ko"]:
        m = TRAILING_MARK.search(d)
        if m and int(m[1]) >= span[0]:
            marks.append((int(m[1]), int(m[1])))
            d = d[:m.start()].strip()
        desc.append(d)
    if not marks:
        return [p]
    runs = code_runs(p["codes"]) if p["codes"] else [[]]
    if len(marks) == 1 and len(runs) == 1:
        lo, hi = max(marks[0][0], span[0]), min(marks[0][1], span[1])
        return [dict(p, years=fmt(lo, hi), notes_ko=keep, desc_ko=desc)]
    if len(marks) == len(runs):
        out = []
        for (lo, hi), run in zip(marks, runs):
            lo, hi = max(lo, span[0]), min(hi, span[1])
            out.append(dict(copy.deepcopy(p), years=fmt(lo, hi), codes=run, notes_ko=keep, desc_ko=desc))
        return out
    return [p]


SINCE_2009 = re.compile(r"^\(2009년\s*이후\)$")


def split_since_2009(p: dict) -> list[dict]:
    """HEALS lists the 2002-2008 and 2009+ codes in one cell, marked '(2009년이후)'."""
    if not any(SINCE_2009.match(d) for d in p["desc_ko"]):
        return [p]
    runs = code_runs(p["codes"])
    span = bounds(p["years"])
    if len(runs) != 2 or not span:
        return [p]
    desc = [d for d in p["desc_ko"] if not SINCE_2009.match(d)]
    early, late = runs
    out = []
    if span[0] < 2009:
        out.append(dict(copy.deepcopy(p), years=fmt(span[0], min(span[1], 2008)), codes=early, desc_ko=desc))
    if span[1] >= 2009:
        q = dict(copy.deepcopy(p), years=fmt(max(span[0], 2009), span[1]), codes=late, desc_ko=desc)
        if span[0] >= 2009:
            q["notes_en"] = q["notes_en"] + [
                "The source cell also lists the coding used before 2009 ("
                + ", ".join(f"{c['code']} {_tr(c['label_ko']).lower()}" for c in early)
                + "), which does not apply to these years."]
        out.append(q)
    return out


def merge_periods(v: dict) -> None:
    """Merge adjacent periods whose content became identical after curation."""
    out: list[dict] = []
    for p in sorted(v["periods"], key=lambda p: p["years"]):
        for q in out:
            if same_content(q, p) and q.get("notes_en") == p.get("notes_en"):
                q["years"] = merge_years(q["years"], p["years"])
                break
        else:
            out.append(p)
    v["periods"] = out


def flag_duplicate_codes(v: dict) -> None:
    for p in v["periods"]:
        codes = [c["code"] for c in p["codes"]]
        if len(codes) != len(set(codes)):
            p["notes_en"].append(
                "The source lists more than one meaning for the same code in these years, "
                "so the codes are reproduced as printed. Check the coding against your extract.")


# --- Helpers ----------------------------------------------------------------

def find(t: dict, name: str) -> dict:
    for v in t["variables"]:
        if v["name"] == name:
            return v
    raise KeyError(f"{t['id']}.{name} not found")


def period(v: dict, years: str) -> dict:
    """Return the period covering exactly `years`, splitting a wider period if needed."""
    lo, hi = bounds(years)
    for i, p in enumerate(v["periods"]):
        for part in p["years"].split(","):
            span = bounds(part.strip())
            if not span or not (span[0] <= lo and hi <= span[1]):
                continue
            if p["years"] == years:
                return p
            pieces = [y.strip() for y in p["years"].split(",") if y.strip() != part.strip()]
            if span[0] < lo:
                pieces.append(fmt(span[0], lo - 1))
            if hi < span[1]:
                pieces.append(fmt(hi + 1, span[1]))
            target = copy.deepcopy(p)
            target["years"] = years
            rest = []
            for y in pieces:
                q = copy.deepcopy(p)
                q["years"] = y
                rest.append(q)
            v["periods"][i:i + 1] = rest + [target]
            return target
    raise KeyError(f"{v['name']} has no period {years}")
