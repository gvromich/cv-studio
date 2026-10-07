#!/usr/bin/env bash
# One-shot setup for the claude.ai / Claude Desktop sandbox (also fine locally).
# Installs dependencies, makes sure a Chromium is available, and runs the smoke
# test. Safe to run more than once. Prints CV-STUDIO READY on success.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -d node_modules/playwright ]; then
  PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci --no-audit --no-fund --silent
fi

# Use a preinstalled Chromium if there is one; otherwise try Playwright's download.
if ! node -e "import('./lib/chromium-launch.mjs').then(async m => { const b = await m.launchChromium({ headless: true }); await b.close(); })" 2>/dev/null; then
  echo "No usable Chromium found, trying Playwright download..."
  npx playwright install chromium
fi

mkdir -p output jds
npm run --silent smoke > output/_smoke.log 2>&1 || { cat output/_smoke.log; echo "CV-STUDIO SETUP FAILED"; exit 1; }
echo "CV-STUDIO READY ($(node -v), $(grep -o 'Pages: [0-9]*' output/_smoke.log))"
