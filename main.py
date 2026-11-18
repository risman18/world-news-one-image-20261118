#!/usr/bin/env python3
"""Deliver the finished front page: copy entry.png to /output/entry.png.

The output is a byte-identical copy of the entry.png stored next to
this script in the repository root, so every run produces exactly
the same file. Standard library only; no network access.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "entry.png"
DST_DIR = Path("/output")
DST = DST_DIR / "entry.png"


def main() -> None:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
