// Deck → PPTX for Canva import: every slides/*.png full-bleed, presenter notes from NOTES.md.
// Run (pptxgenjs lives in the session scratchpad, not here):
//   NODE_PATH=<scratchpad>/node_modules node build-deck.js
const pptxgen = require('pptxgenjs'); const JSZip = require('jszip'); const fs = require('fs'); const path = require('path');
const OUT = process.argv[2] || 'letting-go-talk.pptx';

const notes = {}; let cur = null;
for (const line of fs.readFileSync('NOTES.md', 'utf8').split(/\r?\n/)) {
  const m = line.match(/^## (\S+)\s*$/);
  if (m) { cur = m[1]; notes[cur] = []; continue; }
  if (cur) notes[cur].push(line);
}
for (const k in notes) notes[k] = notes[k].join('\n').trim();

const files = fs.readdirSync('slides').filter(f => f.endsWith('.png')).sort();
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.title = 'Why letting go is a high-agency skill';
const missing = [];
for (const f of files) {
  const name = f.replace(/\.png$/, ''); const s = pres.addSlide();
  s.addImage({ path: path.join('slides', f), x: 0, y: 0, w: 10, h: 5.625 });
  if (notes[name]) s.addNotes(notes[name]); else missing.push(name);
}
pres.writeFile({ fileName: OUT }).then(async () => {
  // Canva chokes on the slide-number shape pptxgenjs puts in every notes slide: strip it.
  const zip = await JSZip.loadAsync(fs.readFileSync(OUT));
  for (const n of Object.keys(zip.files)) if (/^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(n)) {
    const x = await zip.file(n).async('string');
    zip.file(n, x.replace(/<p:sp>(?:(?!<\/p:sp>)[\s\S])*?type="sldNum"(?:(?!<\/p:sp>)[\s\S])*<\/p:sp>/g, ''));
  }
  fs.writeFileSync(OUT, await zip.generateAsync({ type: 'nodebuffer' }));
  console.log(`${OUT}: ${files.length} slides, notes missing for: ${missing.length ? missing.join(', ') : 'none'}`);
});
