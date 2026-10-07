#!/usr/bin/env python3
"""Check the CV Versions table against cv.md.

Usage:
  python3 scripts/check-versions.py <versions.csv> [--cv cv.md] [--base64]

A version (preset) may only choose and reorder what cv.md already has. This
checks the parts of each row that end up on the page:
  - every Competencies item (";"-separated) appears in cv.md,
  - every Skills order category is a "**Category:**" heading in cv.md's Skills.
Prints one line per version, then any problems. Exit 0 ok, 2 problems found.
"""
import argparse
import base64
import csv
import io
import re
import sys


def norm(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--cv", default="cv.md")
    ap.add_argument("--base64", action="store_true")
    a = ap.parse_args()
    raw = open(a.src, encoding="utf-8").read()
    text = base64.b64decode(raw.strip()).decode("utf-8") if a.base64 else raw
    cv = open(a.cv, encoding="utf-8").read()
    cv_n = norm(cv)
    skill_cats = {norm(c) for c in re.findall(r"^- \*\*(.+?):\*\*", cv, flags=re.M)}

    rows = list(csv.DictReader(io.StringIO(text)))
    problems = []
    for r in rows:
        name = (r.get("Version") or "").strip()
        if not name:
            continue
        code = (r.get("Code") or "").strip()
        comps = [c.strip() for c in (r.get("Competencies") or "").split(";") if c.strip()]
        cats = [c.strip() for c in (r.get("Skills order") or "").split(",") if c.strip()]
        print(f"{code or '?'}  {name}: {len(comps)} competencies, {len(cats)} skill groups")
        if not code:
            problems.append(f"{name}: Code is empty (use a short code like BA)")
        for c in comps:
            if norm(c) not in cv_n:
                problems.append(f'{name}: competency "{c}" is not in the Master CV')
        for c in cats:
            if norm(c) not in skill_cats:
                problems.append(f'{name}: skill group "{c}" is not a group in the Master CV Skills section')
    if not rows:
        problems.append("the Versions table has no rows")
    if problems:
        print("\nProblems:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(2)
    print("All versions use only what the Master CV contains.")


if __name__ == "__main__":
    main()
