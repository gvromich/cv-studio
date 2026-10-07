# cv-studio

Tailored, fact-checked CVs from a baseline CV. Runs from claude.ai, Claude Desktop or Claude Code.

```
find jobs (Indeed connector)  ->  /tailor-cv <job>  ->  output/{company}-{role}.pdf
                                  /cover-letter <job> ->  output/{company}-{role}-cover.pdf
```

## Use in claude.ai or Claude Desktop (no local install, no GitHub)

The claude.ai skill is self-contained: it carries this whole app in its `app/` folder, and Elena's facts live in Google Drive. Nothing is cloned from GitHub at runtime.

1. Build the skill: `python3 scripts/build-skill.py` writes `dist/cv-studio.skill` (and `dist/cv-studio-skill.zip`, the same file for the Settings upload button).
2. Install it once per Claude account: open `cv-studio.skill` in a chat and click **Save skill**, or upload the zip under Settings → Capabilities → Skills.
3. Turn on code execution (network egress "package managers" is enough), the Indeed connector and Google Drive.
4. In any chat: "find business analyst roles in Chicago posted this week", then "CVs for 2 and 5".

Elena's facts and role presets live in a Drive folder named `cv-studio profile`: the **Master CV** (Google Doc, the single source of facts), **CV Versions** (Google Sheet with one preset per role type) and a short guide. Each run imports the Doc into `cv.md`, reports what changed since the last run, and checks the presets. She updates her CV by editing the Doc, by telling Claude in chat, or by attaching a new resume.

When the code, templates, `CLAUDE.md` or the procedures change, rebuild the skill and save it again in each account that uses it. Changes to the Master CV or CV Versions need no rebuild.

## Use in Claude Code

1. Open this folder as the Claude Code project (it reads `CLAUDE.md` and the commands in `.claude/commands/`).
2. Search for jobs with the Indeed connector as you normally would.
3. Pick one and run `/tailor-cv <Indeed link, job id, or pasted description>`.
4. Optionally run `/cover-letter <same job>`.

Every run: saves the JD to `jds/`, checks the JD's skills against `cv.md`, tailors the content, builds the HTML, runs the fact gate (a hard stop on any invented metric or fact), renders the PDF and reports page count, keyword coverage and unaddressed skill gaps.

## Setup (Claude Code, once per machine)

```bash
npm run setup          # npm install + Playwright Chromium
npm run smoke          # self-test: build, fact gate, render the baseline sample
```

In a sandbox that can't download browsers (claude.ai, Claude Desktop chats), use `npm run setup:sandbox` instead. `lib/chromium-launch.mjs` finds the preinstalled Chromium on its own; set `CHROMIUM_PATH` to force a specific binary.

## Files you edit

- `cv.md` — the baseline CV and the only source of facts. Change it first when something about Elena's experience changes.
- `config/profile.yml` — contact details printed on the CV.
- `config/cv-facts.json` — verified exceptions and forbidden phrases for the fact gate.
- `CLAUDE.md` — rules and house style the commands follow.

`output/` and `jds/` are gitignored. `cv.md` and `config/profile.yml` contain personal contact details, so keep any remote for this project private. The claude.ai route doesn't need GitHub at all.

## Origin

The generator (`build-cv-html.mjs`, `generate-pdf.mjs`, `verify-cv-facts.mjs`, `jd-skill-gap.mjs`, `skill-extract.mjs`, `generate-cover-letter.mjs`, templates and fonts) was extracted from the career-ops repo and detached from its tracker, reports and web UI. `tests/baseline-servicenow.*` is a CV produced by the original pipeline, used as the render smoke test.
