# cv-studio

Tailored, fact-checked CVs from a baseline CV, driven by Claude Code commands.

```
find jobs (Indeed connector)  ->  /tailor-cv <job>  ->  output/{company}-{role}.pdf
                                  /cover-letter <job> ->  output/{company}-{role}-cover.pdf
```

## Use

1. Open this folder as the Claude Code project (it reads `CLAUDE.md` and the commands in `.claude/commands/`).
2. Search for jobs with the Indeed connector as you normally would.
3. Pick one and run `/tailor-cv <Indeed link, job id, or pasted description>`.
4. Optionally run `/cover-letter <same job>`.

Every run: saves the JD to `jds/`, checks the JD's skills against `cv.md`, tailors the content, builds the HTML, runs the fact gate (a hard stop on any invented metric or fact), renders the PDF and reports page count, keyword coverage and unaddressed skill gaps.

## Setup (once per machine)

```bash
npm run setup      # npm install + Playwright Chromium
npm run smoke      # self-test: build, fact gate, render the baseline sample
```

## Files you edit

- `cv.md` — the baseline CV and the only source of facts. Change it first when something about Elena's experience changes.
- `config/profile.yml` — contact details printed on the CV.
- `config/cv-facts.json` — verified exceptions and forbidden phrases for the fact gate.
- `CLAUDE.md` — rules and house style the commands follow.

`output/` and `jds/` are gitignored. `cv.md` and `config/profile.yml` contain personal contact details, so keep any remote for this repo private.

## Origin

The generator (`build-cv-html.mjs`, `generate-pdf.mjs`, `verify-cv-facts.mjs`, `jd-skill-gap.mjs`, `skill-extract.mjs`, `generate-cover-letter.mjs`, templates and fonts) was extracted from the career-ops repo and detached from its tracker, reports and web UI. `tests/baseline-servicenow.*` is a CV produced by the original pipeline, used as the render smoke test.
