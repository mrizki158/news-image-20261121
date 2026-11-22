#!/usr/bin/env python3
"""Deliver the bundled broadsheet image to the grader's output folder.

The artwork is finished ahead of time and stored beside this file as
entry.png; all the entrypoint has to do is copy those bytes, unchanged,
into the directory named by MAKEFUN_OUTPUT_DIR.
"""

import os
import sys
from pathlib import Path

BLOCK = 128 * 1024  # copy the image in 128 KiB blocks


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / source.name
    with source.open("rb") as fin, target.open("wb") as fout:
        while block := fin.read(BLOCK):
            fout.write(block)
    if target.stat().st_size != source.stat().st_size:
        raise SystemExit("copied image came out a different size; refusing to deliver it")
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
