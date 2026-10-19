"""Generate the Variables section of the site from the YAML files in codebook/.

Run automatically by the mkdocs-gen-files plugin on every `mkdocs serve` and
`mkdocs build`. The generated pages exist only in the build; edit the YAML
files, never the generated Markdown.

Layout of codebook/:

    codebook/<dataset>/_dataset.yml   one per dataset (title, years, sources, order)
    codebook/<dataset>/_codes.yml     optional shared code lists
    codebook/<dataset>/<table>.yml    one per table, with its variables

Pages generated under variables/:

    index.md                          list of datasets
    <dataset>/index.md                every variable of the dataset, grouped by table
    <dataset>/<table>/<variable>.md   one page per variable
    <dataset>/codes/<list>.md         one page per shared code list

See docs/about/contributing.md for the field reference.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import mkdocs_gen_files
import yaml

ROOT = Path(__file__).resolve().parent.parent
CODEBOOK = ROOT / "codebook"
OUT = Path("variables")

STATUSES = {
    "documented": "Documented",
    "verified": "Verified",
    "unverified": "Unverified",
    "disputed": "Disputed",
}
DATASET_REQUIRED = ["id", "title", "title_ko", "years"]
TABLE_REQUIRED = ["id", "title", "title_ko", "variables"]
VARIABLE_REQUIRED = ["name", "label_ko", "label_en", "status"]
GROUPS = {"basic": "Basic tables", "additional": "Additional tables"}
INLINE_CODES = 60  # shared code lists up to this length are also shown on the variable page


class CodebookError(Exception):
    pass


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise CodebookError(f"{path}: expected a mapping at the top level")
    return data


def require(obj: dict, fields: list[str], where: str) -> None:
    missing = [f for f in fields if obj.get(f) in (None, "", [])]
    if missing:
        raise CodebookError(f"{where}: missing required field(s) {', '.join(missing)}")


def check_status(obj: dict, where: str) -> None:
    status = obj.get("status")
    if status not in STATUSES:
        raise CodebookError(
            f"{where}: status must be one of {', '.join(STATUSES)}, got {status!r}"
        )
    if status == "verified":
        require(obj, ["verified_by", "verified_on"], where)


def slug(name: str) -> str:
    return name.lower()


def cell(text) -> str:
    """Make a value safe for a one-line Markdown table cell."""
    if text is None:
        return ""
    return " ".join(str(text).split()).replace("|", "\\|").replace("<", "&lt;")


def badge(status: str) -> str:
    return f'<span class="status status-{status}">{STATUSES[status]}</span>'


# --- Loading ----------------------------------------------------------------

def normalize(v: dict) -> None:
    """Give an entry written in the flat form (values, description) a single period."""
    if v.get("periods"):
        return
    p = {"years": v.get("years", ""), "label_ko": v["label_ko"], "label_en": v["label_en"]}
    if v.get("description"):
        p["description"] = [{"en": " ".join(v["description"].split())}]
    if v.get("values"):
        p["codes"] = v["values"]
    v["periods"] = [p]
    v.pop("description", None)


def load_codebook() -> list[dict]:
    datasets = []
    for ds_dir in sorted(p for p in CODEBOOK.iterdir() if p.is_dir()):
        meta_path = ds_dir / "_dataset.yml"
        if not meta_path.exists():
            raise CodebookError(f"{ds_dir}: missing _dataset.yml")
        ds = load_yaml(meta_path)
        require(ds, DATASET_REQUIRED, str(meta_path))
        if ds["id"] != ds_dir.name:
            raise CodebookError(f"{meta_path}: id {ds['id']!r} must match folder name")
        codes_path = ds_dir / "_codes.yml"
        ds["code_lists"] = load_yaml(codes_path) if codes_path.exists() else {}

        tables = []
        for t_path in sorted(ds_dir.glob("*.yml")):
            if t_path.name.startswith("_"):
                continue
            t = load_yaml(t_path)
            require(t, TABLE_REQUIRED, str(t_path))
            if t["id"] != t_path.stem:
                raise CodebookError(f"{t_path}: id {t['id']!r} must match file name")
            seen = set()
            for v in t["variables"]:
                where = f"{t_path}: variable {v.get('name', '?')}"
                require(v, VARIABLE_REQUIRED, where)
                check_status(v, where)
                if slug(v["name"]) in seen:
                    raise CodebookError(f"{where}: duplicate variable name")
                seen.add(slug(v["name"]))
                normalize(v)
                for p in v["periods"]:
                    ref = p.get("code_list")
                    if ref and ref not in ds["code_lists"]:
                        raise CodebookError(f"{where}: unknown code list {ref!r}")
            t["_source"] = t_path.relative_to(ROOT).as_posix()
            tables.append(t)
        tables.sort(key=lambda t: (t.get("order", 99), t["id"]))
        ds["tables"] = tables
        datasets.append(ds)
    datasets.sort(key=lambda d: (d.get("order", 99), d["id"]))
    return datasets


# --- Links ------------------------------------------------------------------

def var_link(ds_id: str, t_id: str, name: str, here: tuple[str, str] | None) -> str:
    """Relative path to a variable page, from a variable page in `here` or from the index."""
    target = f"{ds_id}/{t_id}/{slug(name)}.md"
    if here is None:
        return target
    if here[0] == ds_id:
        return f"../{t_id}/{slug(name)}.md" if here[1] != t_id else f"{slug(name)}.md"
    return f"../../{target}"


def resolve_related(ref: str, ds_id: str, t_id: str, index: dict, where: str) -> str:
    """Turn 'VAR', 'table.VAR', or 'dataset.table.VAR' into a link to that variable's page."""
    parts = ref.split(".")
    if len(parts) == 1:
        parts = [ds_id, t_id, *parts]
    elif len(parts) == 2:
        parts = [ds_id, *parts]
    if len(parts) != 3 or (parts[0], parts[1], slug(parts[2])) not in index:
        raise CodebookError(f"{where}: related entry {ref!r} does not match any variable")
    r_ds, r_table, r_var = parts
    label = r_var if (r_ds, r_table) == (ds_id, t_id) else ".".join(parts if r_ds != ds_id else parts[1:])
    return f"[`{label}`]({var_link(r_ds, r_table, r_var, (ds_id, t_id))})"


# --- Rendering pieces -------------------------------------------------------

def bilingual_rows(items: list[dict]) -> list[str]:
    """A two-column table of English text and the Korean original, or a list if there is none."""
    if not any(it.get("ko") for it in items):
        return [f"- {' '.join(str(it.get('en', '')).split())}" for it in items] + [""]
    lines = ["| English | 원문 (Korean original) |", "|---|---|"]
    for it in items:
        lines.append(f"| {cell(it.get('en'))} | {cell(it.get('ko'))} |")
    return lines + [""]


def code_rows(codes: list[dict], english: bool = True) -> list[str]:
    head = "| Code | 한글 | English |" if english else "| Code | 한글 |"
    lines = [head, "|---|---|---|" if english else "|---|---|"]
    for c in codes:
        if "section_ko" in c:
            row = f"| | **{cell(c['section_ko'])}** |"
            lines.append(row + (f" **{cell(c.get('section_en'))}** |" if english else ""))
            continue
        row = f"| `{cell(c.get('code'))}` | {cell(c.get('label_ko'))} |"
        lines.append(row + (f" {cell(c.get('label_en'))} |" if english else ""))
    return lines + [""]


def code_list_title(name: str, lst: dict) -> str:
    return f"{lst.get('title', name)} ({name})"


def render_period(p: dict, v: dict, ds: dict, level: str) -> list[str]:
    lines = []
    if p.get("label_ko") and p["label_ko"] != v["label_ko"]:
        lines += [f"**Label in these years** {cell(p['label_ko'])} · {cell(p.get('label_en'))}", ""]
    if p.get("type"):
        lines += [f"**Type** {cell(p['type'])}", ""]
    if p.get("description"):
        lines += [f"{level} Description", ""] + bilingual_rows(p["description"])
    if p.get("codes"):
        lines += [f"{level} Codes", ""] + code_rows(p["codes"])
    if p.get("code_list"):
        name = p["code_list"]
        lst = ds["code_lists"][name]
        link = f"../codes/{slug(name)}.md"
        lines += [f"{level} Codes", "",
                  f"Codes come from the shared list [{code_list_title(name, lst)}]({link}), "
                  f"which has {sum('code' in c for c in lst['codes'])} entries.", ""]
        if len(lst["codes"]) <= INLINE_CODES and not lst.get("groups"):
            lines += code_rows(lst["codes"])
    if p.get("notes"):
        lines += [f"{level} Notes", ""] + bilingual_rows(p["notes"])
    return lines


def render_variable(v: dict, t: dict, ds: dict, index: dict, by_name: dict) -> str:
    where = f"{t['_source']}: variable {v['name']}"
    short = ds.get("short", ds["title"])
    lines = [
        "---",
        "title: " + json.dumps(f"{v['name']} ({short}, {t['title']})", ensure_ascii=False),
        "---",
        "",
        f"[Variables](../../index.md) › [{ds['title']}](../index.md) › "
        f"[{t['title']}](../index.md#{t['id']})",
        "",
        f"# {v['name']}",
        "",
        f"**{cell(v['label_ko'])}** · {cell(v['label_en'])} {badge(v['status'])}",
        "",
        f"- **Dataset** {ds['title']} ({ds['title_ko']})",
        f"- **Table** {t['title']} · {cell(t['title_ko'])}",
    ]
    if v.get("type"):
        lines.append(f"- **Type** {cell(v['type'])}")
    if v.get("years"):
        lines.append(f"- **Years** {cell(v['years'])}")
    lines.append(f"- **Source** {cell(t.get('source', ''))}")
    if v["status"] == "verified":
        lines.append(f"- **Verified** {v['verified_by']}, {v['verified_on']}")
    lines.append("")

    if v.get("notes"):
        lines += ['!!! note "Notes"', ""]
        lines += [f"    - {' '.join(str(n).split())}" for n in v["notes"]]
        lines.append("")

    periods = v["periods"]
    if len(periods) == 1:
        lines += render_period(periods[0], v, ds, "##")
    else:
        lines += [
            "The documentation describes this variable differently in different years, "
            "so each period is shown separately.",
            "",
        ]
        for p in periods:
            lines += [f"## {p['years']}", ""] + render_period(p, v, ds, "###")

    if v.get("related"):
        links = [resolve_related(r, ds["id"], t["id"], index, where) for r in v["related"]]
        lines += ["## Related", "", ", ".join(links), ""]

    others = [o for o in by_name[v["name"]] if (o[0]["id"], o[1]["id"]) != (ds["id"], t["id"])]
    if others:
        lines += ["## Same name in other tables", ""]
        for o_ds, o_t, o_v in others:
            link = var_link(o_ds["id"], o_t["id"], o_v["name"], (ds["id"], t["id"]))
            lines.append(f"- [{o_ds.get('short', o_ds['title'])}, {o_t['title']}]({link}) "
                         f"· {cell(o_v['label_ko'])} · {cell(o_v['label_en'])}")
        lines.append("")
    return "\n".join(lines)


def render_code_list(name: str, lst: dict, ds: dict, users: list) -> str:
    lines = [
        f"[Variables](../../index.md) › [{ds['title']}](../index.md) › Code lists",
        "",
        f"# {code_list_title(name, lst)}",
        "",
        f"{ds['title']} ({ds['title_ko']})",
        "",
    ]
    if users:
        links = [f"[`{v['name']}`](../{t['id']}/{slug(v['name'])}.md) ({t['title']})" for t, v in users]
        lines += ["Used by " + ", ".join(links) + ".", ""]
    if lst.get("notes"):
        lines += bilingual_rows(lst["notes"])
    if lst.get("groups"):
        by_group = defaultdict(list)
        for c in lst["codes"]:
            by_group[c.get("group", "")].append(c)
        for g, entries in sorted(by_group.items()):
            label = lst["groups"].get(g, {})
            heading = f"{g} {label.get('label_en', '')}".strip()
            lines += [f"## {heading}", "", cell(label.get("label_ko", "")), ""]
            lines += code_rows(entries, english=False)
    else:
        lines += code_rows(lst["codes"])
    return "\n".join(lines)


def variable_rows(t: dict, ds: dict) -> list[str]:
    lines = ["| Variable | 한글 | English | Years |", "|---|---|---|---|"]
    for v in t["variables"]:
        status = "" if v["status"] == "documented" else " " + badge(v["status"])
        lines.append(
            f"| [`{v['name']}`]({t['id']}/{slug(v['name'])}.md) | {cell(v['label_ko'])} | "
            f"{cell(v['label_en'])}{status} | {cell(v.get('years'))} |"
        )
    return lines + [""]


def render_dataset(ds: dict, code_users: dict) -> str:
    n_vars = sum(len(t["variables"]) for t in ds["tables"])
    lines = [
        "[Variables](../index.md) › " + ds["title"],
        "",
        f"# {ds['title']} ({ds['title_ko']})",
        "",
    ]
    if ds.get("description"):
        lines += [ds["description"].strip(), ""]
    lines += [
        f"This page lists all {n_vars:,} variables of the {ds['title']} in {len(ds['tables'])} tables, "
        "as described in the NHIS documentation listed below. Select a variable to see its Korean "
        "and English names, its description, and the meaning of each code.",
        "",
    ]
    if ds.get("page"):
        lines += [f"Background on sampling, versions, and linkage is on the [dataset page](../../{ds['page']}).", ""]
    if ds.get("sources"):
        lines += ["**Sources**", ""]
        for s in ds["sources"]:
            date = f", {s['date']}" if s.get("date") else ""
            lines.append(f"- {s['title']}{date} (`{s['file']}`)")
        lines.append("")

    lines += ["## Tables", "", "| Table | 한글 | Variables |", "|---|---|---|"]
    for t in ds["tables"]:
        lines.append(f"| [{t['title']}](#{t['id']}) | {cell(t['title_ko'])} | {len(t['variables'])} |")
    lines.append("")

    grouped = any(t.get("group") for t in ds["tables"])
    current = None
    for t in ds["tables"]:
        level = "##"
        if grouped:
            level = "###"
            if t.get("group") != current:
                current = t.get("group")
                lines += [f"## {GROUPS.get(current, current)}", ""]
        lines += [f"{level} {t['title']} {{ #{t['id']} }}", "", cell(t["title_ko"]), ""]
        facts = [
            ("Files", ", ".join(f"`{f.strip()}`" for f in t["files"].split(",")) if t.get("files") else None),
            ("Unit of observation", t.get("unit")),
            ("Source", f"`{t['source']}`" if t.get("source") else None),
        ]
        lines += [f"- **{k}** {val}" for k, val in facts if val]
        lines.append("")
        if t.get("description"):
            lines += [t["description"].strip(), ""]
        lines += variable_rows(t, ds)

    if ds["code_lists"]:
        lines += ["## Code lists", "", "| List | Entries | Used by |", "|---|---|---|"]
        for name, lst in ds["code_lists"].items():
            users = ", ".join(f"`{v['name']}`" for _, v in code_users.get(name, []))
            n = sum("code" in c for c in lst["codes"])
            lines.append(f"| [{code_list_title(name, lst)}](codes/{slug(name)}.md) | {n} | {users} |")
        lines.append("")
    return "\n".join(lines)


def render_index(datasets: list[dict]) -> str:
    n_vars = sum(len(t["variables"]) for ds in datasets for t in ds["tables"])
    counts = defaultdict(int)
    for ds in datasets:
        for t in ds["tables"]:
            for v in t["variables"]:
                counts[v["status"]] += 1
    lines = [
        "# Variables",
        "",
        "This section documents every table and variable of each NHIS research database. "
        f"It currently covers {n_vars:,} variables in {len(datasets)} datasets. Choose a dataset "
        "to see all its variables grouped by table, then select a variable to see its Korean and "
        "English names, its description, and the meaning of each code.",
        "",
        "| Dataset | 한글 | Years | Tables | Variables |",
        "|---|---|---|---|---|",
    ]
    for ds in datasets:
        n = sum(len(t["variables"]) for t in ds["tables"])
        lines.append(
            f"| [{ds['title']}]({ds['id']}/index.md) | {cell(ds['title_ko'])} | "
            f"{cell(ds['years'])} | {len(ds['tables'])} | {n:,} |"
        )
    lines += [
        "",
        "## Status of entries",
        "",
        "Each entry carries a status badge, and the counts below cover the whole codebook.",
        "",
        f"- {badge('documented')} The entry is imported from the NHIS layout files and manuals "
        f"and translated, but not checked against the data ({counts['documented']:,} entries).",
        f"- {badge('verified')} The entry has been checked against the data, and the person and "
        f"date are recorded ({counts['verified']:,} entries).",
        f"- {badge('unverified')} The entry is drafted from published papers or other secondary "
        f"sources ({counts['unverified']:,} entries).",
        f"- {badge('disputed')} Sources or users disagree, and the notes describe the conflict "
        f"({counts['disputed']:,} entries).",
        "",
        "The English names and descriptions are translations made for this site. The Korean "
        "original is shown next to each translation, and it is the authoritative text. "
        "Corrections are welcome, as described in [Contributing](../about/contributing.md).",
        "",
        "Search for a variable name such as `RN_INDI` or a Korean label such as 주상병 with the "
        "search bar.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    datasets = load_codebook()
    index = set()
    by_name = defaultdict(list)
    for ds in datasets:
        for t in ds["tables"]:
            for v in t["variables"]:
                index.add((ds["id"], t["id"], slug(v["name"])))
                by_name[v["name"]].append((ds, t, v))

    nav = mkdocs_gen_files.Nav()
    nav["Overview"] = "index.md"

    def write(path: Path, text: str, edit: str | None = None) -> None:
        with mkdocs_gen_files.open(OUT / path, "w", encoding="utf-8") as f:
            f.write(text)
        if edit:
            mkdocs_gen_files.set_edit_path(OUT / path, Path("..") / edit)

    write(Path("index.md"), render_index(datasets))
    for ds in datasets:
        code_users = defaultdict(list)
        for t in ds["tables"]:
            for v in t["variables"]:
                for ref in {p.get("code_list") for p in v["periods"]} - {None}:
                    code_users[ref].append((t, v))
        write(Path(ds["id"]) / "index.md", render_dataset(ds, code_users), f"codebook/{ds['id']}/_dataset.yml")
        nav[ds["title"]] = f"{ds['id']}/index.md"
        for t in ds["tables"]:
            for v in t["variables"]:
                write(Path(ds["id"]) / t["id"] / f"{slug(v['name'])}.md",
                      render_variable(v, t, ds, index, by_name), t["_source"])
        for name, lst in ds["code_lists"].items():
            write(Path(ds["id"]) / "codes" / f"{slug(name)}.md",
                  render_code_list(name, lst, ds, code_users.get(name, [])),
                  f"codebook/{ds['id']}/_codes.yml")

    with mkdocs_gen_files.open(OUT / "SUMMARY.md", "w", encoding="utf-8") as f:
        f.writelines(nav.build_literate_nav())


try:
    main()
except CodebookError as e:
    raise SystemExit(f"Codebook error: {e}") from None
