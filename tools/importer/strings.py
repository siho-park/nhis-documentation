"""List every Korean string in the IR files that still lacks an English translation.

Usage: python strings.py <ir_dir> <translations.tsv> <out.tsv>

The output has one string per line with its kind and frequency, sorted so that
related strings sit together. Translations are added to translations.tsv as
'korean<TAB>english' lines.
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

HANGUL = re.compile(r"[가-힣]")
SKIP_LISTS = {"SGG", "INDTP_CD"}  # large lists handled separately


def load_translations(path: pathlib.Path) -> dict:
    out = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "\t" in line and not line.startswith("#"):
                ko, en = line.split("\t", 1)
                out[ko] = en
    return out


def collect(ir_dir: pathlib.Path):
    counter = collections.Counter()
    kinds = {}
    for f in sorted(ir_dir.glob("*.json")):
        ir = json.loads(f.read_text(encoding="utf-8"))
        for t in ir["tables"]:
            yield_str(counter, kinds, t.get("title_ko", ""), "table")
            for v in t["variables"]:
                for p in v["periods"]:
                    yield_str(counter, kinds, p["label_ko"], "label")
                    for d in p["desc_ko"]:
                        yield_str(counter, kinds, d, "desc")
                    for n in p["notes_ko"]:
                        yield_str(counter, kinds, n, "note")
                    for c in p["codes"]:
                        yield_str(counter, kinds, c["label_ko"], "code")
                        if c.get("group_ko"):
                            yield_str(counter, kinds, c["group_ko"], "code")
        for name, lst in ir.get("code_lists", {}).items():
            if name in SKIP_LISTS:
                continue
            for c in lst:
                yield_str(counter, kinds, c.get("label_ko", ""), "code")
                yield_str(counter, kinds, c.get("note_ko", ""), "note")
                yield_str(counter, kinds, c.get("group_ko", ""), "code")
    return counter, kinds


def yield_str(counter, kinds, s, kind):
    if s and HANGUL.search(s):
        counter[s] += 1
        kinds.setdefault(s, kind)


def main():
    ir_dir, tr, out = map(pathlib.Path, sys.argv[1:4])
    done = load_translations(tr)
    counter, kinds = collect(ir_dir)
    todo = [s for s in counter if s not in done]
    todo.sort(key=lambda s: (kinds[s], s))
    out.write_text("\n".join(f"{kinds[s]}\t{counter[s]}\t{s}" for s in todo), encoding="utf-8")
    print(f"{len(counter)} unique strings, {len(done)} translated, {len(todo)} to do")
    print(collections.Counter(kinds[s] for s in todo))


if __name__ == "__main__":
    main()
