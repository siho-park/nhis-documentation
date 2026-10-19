"""Print an intermediate JSON file in a compact, reviewable form.

Usage: python show.py <ir.json> [table_id ...]
"""

import json
import sys

ir = json.load(open(sys.argv[1], encoding="utf-8"))
only = set(sys.argv[2:])
for t in ir["tables"]:
    if only and t["id"] not in only:
        continue
    print(f"\n## {t['id']}  {t.get('title_ko', '')}  ({len(t['variables'])} variables)")
    for v in t["variables"]:
        for p in v["periods"]:
            codes = "; ".join(f"{c['code']}={c['label_ko']}" for c in p["codes"])
            extra = []
            if p.get("code_ref"):
                extra.append(f"REF={p['code_ref']}")
            if p["desc_ko"]:
                extra.append("D=" + " / ".join(p["desc_ko"]))
            if p["notes_ko"]:
                extra.append("N=" + " / ".join(p["notes_ko"]))
            print(f"- {v['name']} [{p['years']}] {p['label_ko']} <{p['type']}> {' | '.join(extra)}")
            if codes:
                print(f"    codes: {codes[:600]}")
if not only:
    print("\n## code lists")
    for name, lst in ir.get("code_lists", {}).items():
        print(f"- {name}: {len(lst)} entries; first: {lst[:3]}")
