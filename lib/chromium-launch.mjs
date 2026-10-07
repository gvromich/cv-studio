import { chromium } from 'playwright';
import { existsSync, readdirSync } from 'fs';
import { join } from 'path';

// Picks the Chromium that Playwright should launch.
//
// Locally (`npm run setup`), Playwright downloads its own browser and nothing
// here is needed. The claude.ai / Claude Desktop sandbox blocks that download
// but ships a preinstalled Chromium under /opt/pw-browsers, usually a different
// build number than the one this Playwright version expects. Playwright then
// fails with "Executable doesn't exist". This resolver finds a usable binary so
// the same scripts run in both places without flags.
//
// Order: CHROMIUM_PATH env var, then Playwright's own browser if installed,
// then the newest preinstalled build in PLAYWRIGHT_BROWSERS_PATH or
// /opt/pw-browsers. Returns undefined to let Playwright use its default.

const SANDBOX_DIRS = [process.env.PLAYWRIGHT_BROWSERS_PATH, '/opt/pw-browsers'].filter(Boolean);

// Relative binary paths inside a Playwright browser folder, most preferred first.
const CANDIDATES = [
  { prefix: 'chromium_headless_shell-', bins: ['chrome-linux/headless_shell', 'chrome-headless-shell-linux64/chrome-headless-shell'] },
  { prefix: 'chromium-', bins: ['chrome-linux/chrome', 'chrome-linux64/chrome'] },
];

function buildNumber(name) {
  const n = Number(name.split('-').pop());
  return Number.isFinite(n) ? n : -1;
}

function findPreinstalled() {
  for (const dir of SANDBOX_DIRS) {
    let entries;
    try { entries = readdirSync(dir); } catch { continue; }
    for (const { prefix, bins } of CANDIDATES) {
      const builds = entries.filter((e) => e.startsWith(prefix)).sort((a, b) => buildNumber(b) - buildNumber(a));
      for (const build of builds) {
        for (const bin of bins) {
          const p = join(dir, build, bin);
          if (existsSync(p)) return p;
        }
      }
    }
  }
  return undefined;
}

let cached;

/** @returns {string|undefined} an explicit Chromium path, or undefined for Playwright's default */
export function resolveChromiumPath() {
  if (cached !== undefined) return cached || undefined;
  let path;
  if (process.env.CHROMIUM_PATH) {
    path = process.env.CHROMIUM_PATH;
  } else {
    let bundled;
    try { bundled = chromium.executablePath(); } catch { bundled = undefined; }
    path = bundled && existsSync(bundled) ? undefined : findPreinstalled();
  }
  cached = path || '';
  return path;
}

/** Drop-in replacement for chromium.launch(options). */
export function launchChromium(options = {}) {
  const executablePath = resolveChromiumPath();
  return chromium.launch(executablePath ? { ...options, executablePath } : options);
}
