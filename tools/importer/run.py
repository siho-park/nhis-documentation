"""Parse NHIS layout files into intermediate JSON files.

Usage: python run.py <database_dir> <output_dir> [dataset ...]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))


def hwp_text(path: pathlib.Path) -> str:
    """Convert an HWP manual to Markdown-like text with tables (see hwp2md.py)."""
    import tempfile

    import hwp2md

    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "out.md"
        hwp2md.main(str(path), str(out))
        return out.read_text(encoding="utf-8")


def main() -> None:
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    wanted = set(sys.argv[3:])
    out.mkdir(parents=True, exist_ok=True)
    jobs = {
        "nsc": lambda: __import__("parse_nsc").parse(src / "표본코호트DB_사용자매뉴얼" / "표본코호트DB 레이아웃.xlsx"),
        "custom": lambda: __import__("parse_custom").parse(src),
        "heals": lambda: __import__("parse_manual").parse_heals(hwp_text(src / "건강검진코호트DB 사용자 매뉴얼v2.3.hwp")),
        "senior": lambda: __import__("parse_manual").parse_senior(hwp_text(src / "노인코호트DB 매뉴얼v1.4.hwp")),
        "lowrisk": lambda: __import__("parse_manual").parse_lowrisk(hwp_text(src / "표본코호트DB_사용자매뉴얼" / "저위험 표본데이터셋 매뉴얼.hwp")),
    }
    for name, job in jobs.items():
        if wanted and name not in wanted:
            continue
        ir = job()
        (out / f"{name}.json").write_text(json.dumps(ir, ensure_ascii=False, indent=1), encoding="utf-8")
        n = sum(len(t["variables"]) for t in ir["tables"])
        print(f"{name}: {len(ir['tables'])} tables, {n} variables")


if __name__ == "__main__":
    main()
