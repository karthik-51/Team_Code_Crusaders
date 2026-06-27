#!/usr/bin/env python3
"""End-to-end ranking entrypoint (Stages 1-4)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"


def run(script: str, extra_args: list[str] | None = None) -> None:
    cmd = [sys.executable, str(SCRIPTS / script)] + (extra_args or [])
    print(f"\n>>> {' '.join(cmd)}\n")
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Redrob ranker pipeline")
    parser.add_argument(
        "--candidates",
        default=str(ROOT / "dataset" / "candidates.jsonl"),
        help="Path to candidates.jsonl (JSONL format)",
    )
    parser.add_argument(
        "--jd",
        default=str(ROOT / "dataset" / "job_description.docx"),
        help="Path to job description file (.docx, .txt, or .md)",
    )
    parser.add_argument(
        "--out",
        default=str(ROOT / "submission.csv"),
        help="Final submission CSV path",
    )
    parser.add_argument("--skip-stage1", action="store_true")
    parser.add_argument("--skip-stage2", action="store_true")
    parser.add_argument("--skip-stage3", action="store_true")
    args = parser.parse_args()

    # Resolve candidate path relative to ROOT if it's relative
    candidates_path = Path(args.candidates)
    if not candidates_path.is_absolute():
        candidates_path = ROOT / candidates_path
    candidates_path = candidates_path.resolve()

    # Resolve JD path relative to ROOT if it's relative
    jd_path = Path(args.jd)
    if not jd_path.is_absolute():
        jd_path = ROOT / jd_path
    jd_path = jd_path.resolve()

    if not args.skip_stage1:
        run("run_stage1.py", ["--jd", str(jd_path)])
    if not args.skip_stage2:
        run(
            "run_stage2.py",
            [
                "--candidates",
                str(candidates_path),
                "--out",
                str(ROOT / "data" / "precomputed" / "candidate_features_full.jsonl"),
            ],
        )
    if not args.skip_stage3:
        run("run_stage3.py")
    run("run_stage5.py", ["--candidates", str(candidates_path), "--out", args.out])
    run("run_stage6.py", ["--candidates", str(candidates_path), "--out", args.out])


if __name__ == "__main__":
    main()
