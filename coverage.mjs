#!/usr/bin/env node
// coverage.mjs — which JD keywords appear in a generated CV?
//
// Usage: node coverage.mjs output/acme-business-analyst.html "user stories" "backlog" "Jira" ...
//
// Case-insensitive whole-word phrase match against the visible text of the HTML (tags,
// <style> and <script> removed). Prints the hit/miss list and a percentage.
// Advisory only: a missing keyword is a prompt to check cv.md for honest
// evidence, never a reason to invent any.

import { readFileSync } from 'fs';

const [file, ...keywords] = process.argv.slice(2);
if (!file || keywords.length === 0) {
  console.error('Usage: node coverage.mjs <cv.html> "keyword" "keyword" ...');
  process.exit(1);
}

const text = readFileSync(file, 'utf-8')
  .replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<script[\s\S]*?<\/script>/gi, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&amp;/g, '&')
  .replace(/&nbsp;/g, ' ')
  .replace(/\s+/g, ' ')
  .toLowerCase();

const hits = [];
const misses = [];
for (const kw of keywords) {
  const needle = kw.toLowerCase().trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // Whole-word match, so "ERP" is not found inside "enterprise" and "API" not inside "capital".
  const re = new RegExp(`(?<![a-z0-9])${needle}(?![a-z0-9])`);
  (re.test(text) ? hits : misses).push(kw);
}

const pct = Math.round((hits.length / keywords.length) * 100);
console.log(`Keyword coverage: ${hits.length}/${keywords.length} (${pct}%)`);
if (hits.length) console.log(`  present: ${hits.join(', ')}`);
if (misses.length) console.log(`  missing: ${misses.join(', ')}`);
