// News image entry — 20 November 2026.
// The finished picture already exists as entry.png in this directory.
// This script's only job is to place a copy of it where the grader
// expects the entry to land: /output/entry.png (or, while testing on a
// developer machine, the folder named by MAKEFUN_OUTPUT_DIR).
// Nothing is generated or edited here; the PNG is copied byte for byte,
// so the judge sees exactly the image that was made for this date.

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The folder this script lives in — entry.png sits right next to it.
const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourceImage = resolve(scriptDir, 'entry.png');

// Where the finished image must go. Inside the grader the folder is
// always /output; outside it, MAKEFUN_OUTPUT_DIR lets the same script
// be exercised against any scratch directory.
const destinationDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const destinationImage = join(destinationDir, 'entry.png');

if (!existsSync(sourceImage)) {
  throw new Error(`entry.png not found next to main.ts (looked in ${scriptDir})`);
}

// The output folder may not exist yet, so make sure it is there first.
mkdirSync(destinationDir, { recursive: true });

copyFileSync(sourceImage, destinationImage);
console.log(`Wrote ${destinationImage}`);
