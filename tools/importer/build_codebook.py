"""Write codebook/<dataset>/*.yml from the IR, the translations, and the curation rules.

Usage: python build_codebook.py <ir_dir> <translations.tsv> <codebook_dir> [dataset ...]

A variable whose existing YAML entry has status "verified", or carries
"keep: true", is left as it is, so a re-import never overwrites a checked
entry. Every Korean string must have a translation in translations.tsv;
missing strings are listed and the build stops.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from curate import curate  # noqa: E402

HANGUL = re.compile(r"[가-힣]")

DATASETS = {
    "nsc": {
        "title": "National Sample Cohort", "title_ko": "표본코호트DB", "short": "NSC",
        "version": "2.2", "years": "2002-2023", "order": 1, "page": "datasets/nsc.md",
        "sources": [
            {"file": "표본코호트DB 레이아웃.xlsx", "title": "NSC layout, Ver 1.5", "date": "2026-05"},
            {"file": "표본코호트DB 사용자매뉴얼v1.5.hwp", "title": "NSC user manual, v1.5", "date": "2026-05"},
        ],
    },
    "heals": {
        "title": "National Health Screening Cohort", "title_ko": "건강검진코호트DB", "short": "HEALS",
        "years": "2002-2023", "order": 2, "page": "datasets/heals.md",
        "sources": [{"file": "건강검진코호트DB 사용자 매뉴얼v2.3.hwp", "title": "HEALS user manual, v2.3"}],
    },
    "senior": {
        "title": "Senior Cohort", "title_ko": "노인코호트DB", "short": "Senior",
        "years": "2002-2023", "order": 3, "page": "datasets/senior.md",
        "sources": [{"file": "노인코호트DB 매뉴얼v1.4.hwp", "title": "Senior cohort manual, v1.4"}],
    },
    "lowrisk": {
        "title": "Low-Risk Sample Dataset", "title_ko": "저위험 표본데이터셋", "short": "Low-risk",
        "years": "2014-2023", "order": 4, "page": "datasets/low-risk.md",
        "sources": [{"file": "저위험 표본데이터셋 매뉴얼.hwp", "title": "Low-risk sample dataset manual"}],
    },
    "custom": {
        "title": "Customized Research DB", "title_ko": "맞춤형연구DB", "short": "Customized",
        "years": "2002-2024", "order": 5, "page": "datasets/customized.md",
        "sources": [
            {"file": "맞춤형 자료 제공 컬럼 레이아웃_260910.xlsx", "title": "Customized DB column layout", "date": "2026-09-10"},
            {"file": "일반건강검진 자료 제공 컬럼 레이아웃_260910.xlsx", "title": "General health screening column layout", "date": "2026-09-10"},
            {"file": "요양기관 자료 제공 컬럼 레이아웃_260910.xlsx", "title": "Provider column layout", "date": "2026-09-10"},
            {"file": "장기요양 자료 제공 컬럼 레이아웃_260910.xlsx", "title": "Long-term care column layout", "date": "2026-09-10"},
            {"file": "암 검진 자료 제공 컬럼 레이아웃_260910.xlsx", "title": "Cancer screening column layout", "date": "2026-09-10"},
            {"file": "암 문진 자료 제공 컬럼 레이아웃_260910.xlsx", "title": "Cancer screening questionnaire column layout", "date": "2026-09-10"},
            {"file": "영유아건강검진 자료 제공 컬럼 레이아웃_260910.xlsx", "title": "Infant and child screening column layout", "date": "2026-09-10"},
            {"file": "customized_DB_application_2026.xlsx", "title": "Customized DB application form", "date": "2026-07-22"},
        ],
    },
}

# English title, file names, unit of observation. Units are given only where the
# documentation states them.
TABLES = {
    "nsc": {
        "bnc": ("Eligibility and premiums (BNC)", "NSC2_BNC_0215, NSC2_BNC_1619, NSC2_BNC_2023", "Person and year"),
        "bnd": ("Birth and death (BND)", "NSC2_BND", "Person"),
        "t20": ("Claim statements (T20)", "NSC2_M20, NSC2_D20, NSC2_K20, NSC2_P20 (each split into _0215, _1619, _2023)", "Claim"),
        "t30": ("Treatment details (T30)", "NSC2_M30, NSC2_D30, NSC2_K30 (_0215, _1619, _2023); NSC2_P30 (_0208, _0915, _1619, _2023)", "Line item on a claim"),
        "t40": ("Diagnoses (T40)", "NSC2_M40, NSC2_D40, NSC2_K40 (_0215, _1619, _2023)", "Diagnosis on a claim"),
        "t60": ("Prescriptions (T60)", "NSC2_M60, NSC2_D60 (_0215, _1619, _2023)", "Prescribed drug on a claim"),
        "g1e": ("General health screening (G1E)", "NSC2_G1E_0208, NSC2_G1E_0915, NSC2_G1E_1617, NSC2_G1E_1819, NSC2_G1E_2023", "Screening"),
        "inst": ("Healthcare providers (INST)", "NSC2_INST_0215, NSC2_INST_1619, NSC2_INST_2023", "Provider and year"),
        "t01": ("Long-term care applications and results (T01)", "NSC2_T01", None),
        "t02": ("Long-term care assessment items (T02)", "NSC2_T02", None),
        "t04": ("Long-term care claims (T04)", "NSC2_T04", None),
        "t05": ("Long-term care facilities (T05)", "NSC2_T05", None),
    },
    "heals": {
        "jk": ("Eligibility (JK)", "NHIS_HEALS_JK_0215, NHIS_HEALS_JK_1619, NHIS_HEALS_JK_2023", "Person and year"),
        "gy20": ("Claim statements (GY20)", "NHIS_HEALS_GY20_<years>_T1, _T2, _T3", "Claim"),
        "gy30": ("Treatment details (GY30)", "NHIS_HEALS_GY30_<years>_T1, _T2, _T3", "Line item on a claim"),
        "gy40": ("Diagnoses (GY40)", "NHIS_HEALS_GY40_<years>_T1, _T2", "Diagnosis on a claim"),
        "gy60": ("Prescriptions (GY60)", "NHIS_HEALS_GY60_<years>_T1, _T2", "Prescribed drug on a claim"),
        "gj": ("General health screening (GJ)", "NHIS_HEALS_GJ_0215, _1617, _1819, _2023", "Screening"),
        "lj": ("Life-transition health screening (LJ)", "NHIS_HEALS_LJ_0715, NHIS_HEALS_LJ_1617", "Screening"),
        "go": ("Oral screening, general", None, "Screening"),
        "lo": ("Oral screening, life-transition", None, "Screening"),
        "go2": ("Oral screening, general and life-transition combined", None, "Screening"),
        "yk": ("Healthcare providers (YK)", "NHIS_HEALS_YK_0215, NHIS_HEALS_YK_1619, NHIS_HEALS_YK_2023", "Provider and year"),
    },
    "senior": {
        "jk": ("Eligibility (JK)", "NHIS_SENIOR_JK", "Person and year"),
        "gy20": ("Claim statements (GY20)", "NHIS_SENIOR_GY20_T1_<year>, _T2_<year>, _T3_<year>", "Claim"),
        "gy30": ("Treatment details (GY30)", "NHIS_SENIOR_GY30_T1_<year>, _T2_<year>, _T3_<year>", "Line item on a claim"),
        "gy40": ("Diagnoses (GY40)", "NHIS_SENIOR_GY40_T1_<year>, _T2_<year>", "Diagnosis on a claim"),
        "gy60": ("Prescriptions (GY60)", "NHIS_SENIOR_GY60_T1_<year>, _T2_<year>", "Prescribed drug on a claim"),
        "gj": ("Health screening (GJ)", "NHIS_SENIOR_GJ_0217, NHIS_SENIOR_GJ_1819, NHIS_SENIOR_GJ_2023", "Screening"),
        "yk": ("Healthcare providers (YK)", "NHIS_SENIOR_YK", "Provider and year"),
        "t01": ("Long-term care applications and results (T01)", "NHIS_SENIOR_T01", None),
        "t02": ("Long-term care assessment items (T02)", "NHIS_SENIOR_T02", None),
        "t04": ("Long-term care claims (T04)", "NHIS_SENIOR_T04", None),
        "t05": ("Long-term care facilities (T05)", "NHIS_SENIOR_T05", None),
    },
    "lowrisk": {
        "smpl_mc": ("Medical use (SMPL_MC)", "SMPL_MC", "Person, year, and main diagnosis group"),
        "smpl_hc": ("Health screening (SMPL_HC)", "SMPL_HC", None),
    },
    "custom": {
        "bfc": ("Eligibility and premiums (BFC)", "BFC", None),
        "dth": ("Death (DTH)", "DTH", None),
        "t20": ("Claim statements (T20)", "T20", "Claim"),
        "t30": ("Treatment details (T30)", "T30", "Line item on a claim"),
        "t40": ("Diagnoses (T40)", "T40", "Diagnosis on a claim"),
        "t60": ("Prescriptions (T60)", "T60", "Prescribed drug on a claim"),
        "g1e_obj": ("General health screening, eligible population (G1E_OBJ)", "G1E_OBJ", None),
        "gq_rst": ("General health screening, questionnaire (GQ_RST)", "GQ_RST", None),
        "g1e_rst": ("General health screening, results (G1E_RST)", "G1E_RST", None),
        "inst": ("Healthcare providers (INST)", "INST", None),
        "ltc_rcgt": ("Long-term care applications, grades, and assessments", None, None),
        "ltc_clm": ("Long-term care claims", None, None),
        "ltc_inst": ("Long-term care staff and facilities", None, None),
        "ltc_need": ("Long-term care needs assessment", None, None),
        "cst": ("Gastric cancer screening", None, None),
        "clv": ("Liver cancer screening", None, None),
        "ccr": ("Colorectal cancer screening", None, None),
        "cbr": ("Breast cancer screening", None, None),
        "ccx": ("Cervical cancer screening", None, None),
        "clu": ("Lung cancer screening", None, None),
        "cq": ("Cancer screening questionnaire", None, None),
        "inf_tgt": ("Infant and child screening, eligible population", None, None),
        **{f"inf{k}": (f"Infant and child screening, round {k}", None, None) for k in range(8)},
        "mother_child": ("Mother and newborn linkage", None, None),
    },
}

CODE_LISTS = {  # English titles of shared code lists
    "FORM_CD": "Claim form codes", "SUBJ_CD": "Medical specialty codes",
    "DSBJT_CD": "Medical specialty codes", "OFIJ_TYPE": "Work injury type codes",
    "CLA_CD": "Clause (item group) codes", "CLAUSE_CD": "Clause (item group) codes",
    "ITEM_CD": "Item codes", "CLSF_PTTN_CD": "Classification type codes",
    "INST_CLSFC_CD": "Provider type codes", "YKIHO_GUBUN_CD": "Provider type codes",
    "ORG_TYPE": "Provider type codes", "SGG": "District (si, gun, gu) codes",
    "SIDO": "Province codes", "YKIHO_SIDO": "Province codes of the provider",
    "SPCF_SYM_TYPE": "Special code types", "G1E_CHST_XRAY_RST": "Chest X-ray result codes",
    "DISP_SUBJ_CD": "Displayed specialty codes", "DETAIL_TMSG_SUBJ_CD": "Detailed specialty codes",
    "INDTP_CD": "Industry codes (six digits)", "IPSN_TYPE_CD": "Insured type codes",
    "CTRB_PT_TYPE_CD": "Premium decile codes", "DFAB_PTN_CD": "Disability type codes",
    "DIV_TYPE_CD": "Drug classification type codes", "APFRM_TYPE_CD": "Application type codes",
    "LTC_OBJTR_TYPE_CD": "Long-term care recipient type codes",
    "LTC_REDU_TYPE": "Long-term care cost reduction type codes",
    "GJU_RCGT_GRADE_CD": "Long-term care grade codes", "RSDN_TP_CD": "Residence type codes",
    "LVTGT_PRSN_CD": "Household member codes", "CAREPSN_CD": "Main caregiver codes",
    "SIGHT_STAT_CD": "Vision status codes", "HRG_STAT_CD": "Hearing status codes",
    "LTCP_CLSFC_CD": "Long-term care benefit type codes", "ADMIN_KIND_CD": "Facility ownership codes",
    "LTCP_TYPE_CD": "Long-term care benefit category codes",
    "LTCO_FDAT_TYPE_CD": "Facility service type codes", "LTCOS_TYPE_CD": "Facility type codes",
}

KEEP_KO_ONLY = {"INDTP_CD"}  # six-digit industry list; English is given for its groups only


class Translator:
    def __init__(self, path: pathlib.Path):
        self.map = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if "\t" in line:
                ko, en = line.split("\t", 1)
                self.map[ko] = en
        self.missing: set[str] = set()

    def __call__(self, ko: str) -> str:
        if not ko or not HANGUL.search(ko):
            return ko
        en = self.map.get(ko)
        if en is None:
            self.missing.add(ko)
            return ""
        return en


def type_en(raw: str) -> str | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    m = re.fullmatch(r"(?:(문자|숫자)\s*(\d+)|(\d+)\s*(문자|숫자))", raw)
    if m:
        kind = m[1] or m[4]
        size = m[2] or m[3]
        return f"{'Character' if kind == '문자' else 'Numeric'} ({size})"
    m = re.fullmatch(r"(CHR|NUM)\((\d+)\)", raw)
    if m:
        return f"{'Character' if m[1] == 'CHR' else 'Numeric'} ({m[2]})"
    return raw


def years_span(periods: list[dict]) -> str:
    found = [int(y) for p in periods for y in re.findall(r"\d{4}", p["years"])]
    if not found:
        return ""
    lo, hi = min(found), max(found)
    return str(lo) if lo == hi else f"{lo}-{hi}"


def build_period(p: dict, tr: Translator, code_lists: dict) -> dict:
    out = {"years": p["years"], "label_ko": p["label_ko"], "label_en": tr(p["label_ko"])}
    if type_en(p.get("type")):
        out["type"] = type_en(p["type"])
    if p["desc_ko"]:
        out["description"] = [{"ko": d, "en": tr(d)} for d in p["desc_ko"]]
    if p["codes"]:
        out["codes"] = [{"code": c["code"], "label_ko": c["label_ko"], "label_en": tr(c["label_ko"])}
                        for c in p["codes"]]
    if p.get("code_ref"):
        if p["code_ref"] not in code_lists:
            raise SystemExit(f"unknown code list {p['code_ref']}")
        out["code_list"] = p["code_ref"]
    notes = [{"ko": n, "en": tr(n)} for n in p["notes_ko"]] + [{"en": n} for n in p.get("notes_en", [])]
    if notes:
        out["notes"] = notes
    return out


def build_variable(v: dict, tr: Translator, code_lists: dict) -> dict:
    periods = [build_period(p, tr, code_lists) for p in v["periods"]]
    latest = max(periods, key=lambda p: max((int(y) for y in re.findall(r"\d{4}", p["years"])), default=0))
    out = {
        "name": v["name"],
        "label_ko": latest["label_ko"],
        "label_en": latest["label_en"],
        "status": v.get("status", "documented"),
        "years": years_span(v["periods"]),
    }
    types = {p.get("type") for p in periods} - {None}
    if len(types) == 1:
        out["type"] = types.pop()
        for p in periods:
            p.pop("type", None)
    if v.get("notes_en"):
        out["notes"] = list(v["notes_en"])
    out["periods"] = periods
    return out


def build_code_list(name: str, entries: list[dict], tr: Translator, group_labels: dict) -> dict:
    codes, notes = [], []
    for e in entries:
        if "note_ko" in e:
            text = e["note_ko"]
            if not HANGUL.search(text):
                continue  # converter artifacts such as "[nested table below]"
            if len(text) <= 10:  # a sub-heading inside the list, such as 한방
                codes.append({"section_ko": text, "section_en": tr(text)})
            else:
                notes.append({"ko": text, "en": tr(text)})
            continue
        row = {"code": e["code"], "label_ko": e["label_ko"]}
        if name in KEEP_KO_ONLY:
            row["group"] = e["code"][:2]
        else:
            row["label_en"] = tr(e["label_ko"])
        codes.append(row)
    out = {"title": CODE_LISTS.get(name, name), "codes": codes}
    if name in KEEP_KO_ONLY:
        out["groups"] = group_labels
        notes.append({"en": "The six-digit labels are given in Korean only. The first two digits "
                            "identify the industry group, and the group names are translated."})
    if notes:
        out["notes"] = notes
    return out


def existing_variables(path: pathlib.Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {v["name"]: v for v in data.get("variables", [])
            if v.get("status") == "verified" or v.get("keep")}


def dump(path: pathlib.Path, data: dict, header: str) -> None:
    text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)
    path.write_text(header + text, encoding="utf-8")


HEADER = ("# Generated by tools/importer/build_codebook.py from the NHIS documentation.\n"
          "# Entries with status \"verified\" or \"keep: true\" survive a re-import unchanged.\n")


def build_dataset(ds_id: str, ir: dict, tr: Translator, out_root: pathlib.Path) -> int:
    curate(ds_id, ir, tr)
    meta = DATASETS[ds_id]
    out = out_root / ds_id
    out.mkdir(parents=True, exist_ok=True)

    group_labels = {}
    if ds_id == "custom":
        bfc = next(t for t in ir["tables"] if t["id"] == "bfc")
        indtp = next(v for v in bfc["variables"] if v["name"] == "INDTP_CD")
        group_labels = {c["code"]: {"label_ko": c["label_ko"], "label_en": tr(c["label_ko"])}
                        for c in indtp["periods"][0]["codes"]}

    code_lists = {name: build_code_list(name, entries, tr, group_labels)
                  for name, entries in ir.get("code_lists", {}).items()}

    ds_yaml = {"id": ds_id, **{k: v for k, v in meta.items()}}
    dump(out / "_dataset.yml", ds_yaml, HEADER)
    if code_lists:
        dump(out / "_codes.yml", code_lists, HEADER)

    n = 0
    for order, t in enumerate(ir["tables"], 1):
        title, files, unit = TABLES[ds_id][t["id"]]
        path = out / f"{t['id']}.yml"
        keep = existing_variables(path)
        table = {"id": t["id"], "order": order, "title": title, "title_ko": t["title_ko"]}
        if files:
            table["files"] = files
        if unit:
            table["unit"] = unit
        if t.get("group"):
            table["group"] = t["group"]
        table["source"] = t.get("source") or meta["sources"][0]["file"]
        variables = []
        for v in t["variables"]:
            variables.append(keep.get(v["name"]) or build_variable(v, tr, code_lists))
        table["variables"] = variables
        dump(path, table, HEADER)
        n += len(variables)
    return n


def main() -> None:
    ir_dir, tr_path, out_root = map(pathlib.Path, sys.argv[1:4])
    wanted = sys.argv[4:] or list(DATASETS)
    tr = Translator(tr_path)
    for ds_id in wanted:
        ir = json.loads((ir_dir / f"{ds_id}.json").read_text(encoding="utf-8"))
        n = build_dataset(ds_id, ir, tr, out_root)
        print(f"{ds_id}: {n} variables")
    if tr.missing:
        print(f"\n{len(tr.missing)} strings have no translation:")
        for ko in sorted(tr.missing):
            print(f"  {ko}")
        sys.exit(1)


if __name__ == "__main__":
    main()
