import { basename, dirname, join } from 'path';

// generate-pdf.mjs keeps every read and write inside one "workspace" folder and
// derives it from a marker path. cv-studio has no tracker; the marker is only
// a path that lives directly in the project root, so the workspace is the
// project root. Nothing is ever read from or written to it.

export function resolveTrackerPath(rootDir) {
  return join(rootDir, 'data', 'applications.md');
}

export function resolveWorkspaceRoot(markerPath) {
  const dir = dirname(markerPath);
  return basename(dir) === 'data' ? dirname(dir) : dir;
}
