// Render the PNG brand assets from the SVGs that make_logo.py writes:
//   assets/img/apple-touch-icon.png (180x180), assets/img/og-default.png (1200x630)
//   and favicon PNGs (16/32/48) into a temp dir for make_ico.py.
// Usage: node scripts/brand/render.js <tmp-dir>   (needs the `playwright` package)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..', '..');
const img = (f) => fs.readFileSync(path.join(root, 'assets/img', f), 'utf8');
const tmp = process.argv[2];

const page = (body) => `<!doctype html><html><head><style>
  html,body{margin:0;height:100%} svg{display:block;width:100%;height:100%}</style></head><body>${body}</body></html>`;
// Hero waves from index.html, in the light-mode wave tokens.
const waves = `<svg viewBox="0 0 1440 120" preserveAspectRatio="none" style="position:absolute;left:0;bottom:0;width:100%;height:150px">
  <path fill="#D9E8EE" d="M0,64 C240,24 480,104 720,64 C960,24 1200,104 1440,64 L1440,120 L0,120 Z"/>
  <path fill="#B5D3E0" d="M0,84 C200,54 440,114 720,84 C1000,54 1240,114 1440,84 L1440,120 L0,120 Z"/>
  <path fill="#FFFFFF" d="M0,104 C260,84 520,124 720,104 C920,84 1180,124 1440,104 L1440,120 L0,120 Z"/></svg>`;

const jobs = [
  ['assets/img/apple-touch-icon.png', 180, 180, false,
   page(`<div style="background:#FAF6F0;height:100%;padding:18px;box-sizing:border-box">${img('logo-mark.svg')}</div>`)],
  ['assets/img/og-default.png', 1200, 630, false,
   page(`<div style="position:relative;background:#FAF6F0;height:100%;overflow:hidden">
     <div style="position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);width:760px;height:122px">${img('logo.svg')}</div>${waves}</div>`)],
];
for (const px of [16, 32, 48]) jobs.push([path.join(tmp, `favicon-${px}.png`), px, px, true, page(img('favicon.svg'))]);

(async () => {
  const browser = await chromium.launch();
  for (const [out, w, h, transparent, html] of jobs) {
    const p = await browser.newPage({ viewport: { width: w, height: h } });
    await p.setContent(html);
    await p.screenshot({ path: path.isAbsolute(out) ? out : path.join(root, out), omitBackground: transparent });
    await p.close();
  }
  await browser.close();
})();
