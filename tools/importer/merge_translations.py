"""Merge numbered English translations into tools/translations.tsv.

Usage: python merge_translations.py <todo.tsv> <answers.tsv> <translations.tsv>

todo.tsv lines are 'kind<TAB>count<TAB>korean' (line number = id, starting at 1).
answers.tsv lines are 'id<TAB>english'.
"""

import pathlib
import sys

todo_path, ans_path, tr_path = map(pathlib.Path, sys.argv[1:4])
todo = todo_path.read_text(encoding="utf-8").splitlines()
existing = {}
if tr_path.exists():
    for line in tr_path.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            ko, en = line.split("\t", 1)
            existing[ko] = en
added = 0
for line in ans_path.read_text(encoding="utf-8").splitlines():
    if not line.strip() or "\t" not in line:
        continue
    num, en = line.split("\t", 1)
    ko = todo[int(num) - 1].split("\t", 2)[2]
    if ko not in existing:
        added += 1
    existing[ko] = en.strip()
tr_path.write_text("\n".join(f"{k}\t{v}" for k, v in sorted(existing.items())) + "\n",
                   encoding="utf-8")
print(f"added {added}, total {len(existing)}")
