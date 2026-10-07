#!/usr/bin/env python3
"""Bundle cv-studio into a self-contained claude.ai skill.

Usage (from the project root):
  python3 scripts/build-skill.py [--out dist]

Produces:
  dist/cv-studio/              SKILL.md + app/ (the generator, rules and procedures)
  dist/cv-studio.skill         the same folder zipped; open it in Claude and click Save skill
  dist/cv-studio-skill.zip     identical zip, for Settings > Capabilities > Upload skill

The skill copies app/ into the chat's sandbox on first use, so nothing is
fetched from GitHub at runtime. Rebuild and re-save the skill after any change
to the code, templates, CLAUDE.md or the command procedures.
"""
import argparse
import os
import shutil
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_SRC = os.path.join(ROOT, "claude-ai", "cv-studio", "SKILL.md")

# What goes into app/. Paths are relative to the project root.
INCLUDE = [
    "CLAUDE.md", "README.md", "package.json", "package-lock.json", "cv.md",
    ".claude/commands", "config", "fonts", "lib", "templates", "scripts",
    "tests/baseline-servicenow.html",
    "build-cv-html.mjs", "coverage.mjs", "cv-sections-core.mjs", "cv-templates.mjs",
    "generate-cover-letter.mjs", "generate-pdf.mjs", "jd-skill-gap.mjs",
    "path-resolver.mjs", "skill-extract.mjs", "theme-style.mjs",
    "verify-cv-facts.mjs", "workspace.mjs",
]
SKIP_NAMES = {"__pycache__", ".DS_Store", "node_modules"}


def copy(src, dst):
    if os.path.isdir(src):
        for name in sorted(os.listdir(src)):
            if name in SKIP_NAMES:
                continue
            copy(os.path.join(src, name), os.path.join(dst, name))
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"))
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    skill_dir = os.path.join(out, "cv-studio")
    app_dir = os.path.join(skill_dir, "app")
    shutil.rmtree(skill_dir, ignore_errors=True)
    os.makedirs(app_dir)

    shutil.copy2(SKILL_SRC, os.path.join(skill_dir, "SKILL.md"))
    missing = []
    for rel in INCLUDE:
        src = os.path.join(ROOT, rel)
        if not os.path.exists(src):
            missing.append(rel)
            continue
        copy(src, os.path.join(app_dir, rel))
    for d in ("output", "jds"):
        os.makedirs(os.path.join(app_dir, d), exist_ok=True)
        open(os.path.join(app_dir, d, ".gitkeep"), "w").close()
    if missing:
        raise SystemExit(f"Missing from project: {', '.join(missing)}")

    files = 0
    for target in ("cv-studio.skill", "cv-studio-skill.zip"):
        path = os.path.join(out, target)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for dirpath, _, names in os.walk(skill_dir):
                for name in sorted(names):
                    full = os.path.join(dirpath, name)
                    z.write(full, os.path.relpath(full, out))
                    files += 1
    size = os.path.getsize(os.path.join(out, "cv-studio.skill"))
    print(f"Built {out}/cv-studio.skill ({files // 2} files, {size // 1024} KB)")


if __name__ == "__main__":
    main()
