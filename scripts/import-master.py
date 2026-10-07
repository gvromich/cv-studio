#!/usr/bin/env python3
"""Turn the Master CV Google Doc export into cv.md.

Usage:
  python3 scripts/import-master.py <export-file> [--base64] [--out cv.md]

The export is what the Google Drive connector returns for the Master CV with
exportMimeType text/markdown (base64-encoded unless already decoded). Google's
Markdown export escapes punctuation (\\- \\+ \\*), turns emails into mailto
links, adds trailing double spaces as line breaks and may change blank lines.
This script undoes all of that so cv.md is plain text the fact gate can read,
then checks the structure the generator relies on.

Exit codes: 0 ok, 1 unreadable input, 2 structure problem (cv.md not written).
"""
import argparse
import base64
import re
import sys

REQUIRED_SECTIONS = ["Professional Summary", "Work Experience", "Education", "Skills"]


def normalize(md: str) -> str:
    md = md.replace("\r\n", "\n").replace("\u00a0", " ")
    # [text](mailto:...) or [text](http...) -> text
    md = re.sub(r"\[([^\]]+)\]\((?:mailto:|https?://)[^)]*\)", r"\1", md)
    # Backslash escapes Google adds before punctuation
    md = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|>~=])", r"\1", md)
    lines = [ln.rstrip() for ln in md.split("\n")]
    # Bullet markers: Google may export "*" bullets; cv.md uses "-"
    lines = [re.sub(r"^(\s*)\* ", r"\1- ", ln) for ln in lines]
    out, blank = [], False
    for ln in lines:
        if ln == "":
            if not blank and out:
                out.append("")
            blank = True
            continue
        # Keep consecutive bullets tight (no blank line between list items)
        if ln.lstrip().startswith("- ") and out and out[-1] == "" and len(out) > 1 and out[-2].lstrip().startswith("- "):
            out.pop()
        out.append(ln)
        blank = False
    return "\n".join(out).strip() + "\n"


def check(md: str) -> list:
    problems = []
    headings = re.findall(r"^##\s+(.+?)\s*$", md, flags=re.M)
    for sec in REQUIRED_SECTIONS:
        if sec not in headings:
            problems.append(f'missing section "## {sec}"')
    if not re.search(r"^#\s+\S", md, flags=re.M):
        problems.append("missing the top title line (# CV -- Name)")
    if "Work Experience" in headings and not re.search(r"^###\s+\S", md, flags=re.M):
        problems.append('no roles under "## Work Experience" (each role needs a "### Company -- Location" line)')
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--base64", action="store_true", help="input file holds the base64 content field")
    ap.add_argument("--out", default="cv.md")
    a = ap.parse_args()
    try:
        raw = open(a.src, encoding="utf-8").read()
        text = base64.b64decode(raw.strip()).decode("utf-8") if a.base64 else raw
    except Exception as e:  # noqa: BLE001
        print(f"Could not read the export: {e}", file=sys.stderr)
        sys.exit(1)
    md = normalize(text)
    problems = check(md)
    if problems:
        print("Master CV structure problems (cv.md not written):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(2)
    open(a.out, "w", encoding="utf-8").write(md)
    print(f"Wrote {a.out} ({len(md.splitlines())} lines)")


if __name__ == "__main__":
    main()
