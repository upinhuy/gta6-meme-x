// Entry program for make.fun bounty gta6-meme-x-01 ("Post a GTA 6 meme on X").
//
// The entry itself is a post on X; this repository only has to name it.
// POST.json at the repository root holds the post's address, and the
// grader expects to find that file in the output directory after this
// program runs. So the whole job here is: read POST.json from the bot
// directory, make sure it parses and names an X status address, then
// copy it into the output directory.
//
// Outside the grader's sandbox the two directories come from the
// environment: MAKEFUN_BOT_DIR stands in for /bot and
// MAKEFUN_OUTPUT_DIR for /output. Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const sourcePath = join(botDir, 'POST.json');
const targetPath = join(outputDir, 'POST.json');

// Fail loudly rather than hand the grader a file it cannot use.
let post: { url?: unknown };
try {
  post = JSON.parse(readFileSync(sourcePath, 'utf8'));
} catch (err) {
  console.error(`main.ts: cannot read or parse ${sourcePath}: ${(err as Error).message}`);
  process.exit(1);
}

if (typeof post.url !== 'string' || !/^https:\/\/(x\.com|twitter\.com)\/[^/]+\/status\/\d+$/.test(post.url)) {
  console.error(`main.ts: POST.json does not name an X post: ${JSON.stringify(post)}`);
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourcePath, targetPath);

// Read the copy back and compare it with the source: the grader trusts
// whatever lands in the output directory, so a short or corrupted copy
// must fail here instead of failing silently at grading time.
const copied = readFileSync(targetPath, 'utf8');
if (copied !== readFileSync(sourcePath, 'utf8')) {
  console.error(`main.ts: copied POST.json at ${targetPath} differs from ${sourcePath}`);
  process.exit(1);
}
console.log(`main.ts: copied POST.json for ${post.url} to ${targetPath} (${copied.length} bytes, verified)`);
