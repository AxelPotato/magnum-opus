// Called by build_book.py: node tools/book_render.js BOOK.html OUT.pdf OUT-epub.html
// Opens the book page in Chromium, flattens the folds and the form, prints the PDF, then turns every
// figure into a picture (e-readers draw inline SVG and CSS badly) and saves the page for the EPUB.
const { chromium } = require('playwright');
const [src, pdf, out] = process.argv.slice(2);
const FLATTEN = () => {
  document.querySelectorAll('details.say-fold').forEach(d => {
    const div = document.createElement('div');
    div.className = 'fold ' + [...d.classList].filter(c => c.startsWith('k-')).join(' ');
    const k = d.querySelector('.kk'), t = d.querySelector('.tt'), body = d.querySelector('.kb');
    div.innerHTML = '<p class="fk">' + (k ? k.textContent : '') + '</p><h4 class="ft">' + (t ? t.textContent : '') + '</h4>';
    if (body) div.append(...body.childNodes);
    d.replaceWith(div);
  });
  document.querySelectorAll('.contact-form').forEach(f => {
    const p = document.createElement('p');
    p.innerHTML = 'You can leave your details at <a href="https://boringspirituality.com/contact">boringspirituality.com/contact</a>.';
    f.replaceWith(p);
  });
  document.querySelectorAll('script').forEach(s => s.remove());
};
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 700, height: 1000 }, deviceScaleFactor: 2, colorScheme: 'light' });
  await pg.goto('file://' + src, { waitUntil: 'networkidle' });
  await pg.evaluate(FLATTEN);
  await pg.evaluate(() => document.fonts.ready);
  await pg.pdf({ path: pdf, width: '148mm', height: '210mm', printBackground: true,
    margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' }, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;text-align:center;font:9px Georgia,serif;color:#888"><span class="pageNumber"></span></div>' });
  for (const f of await pg.$$('.fig')) {
    if (!(await f.isVisible())) continue;
    await f.evaluate(el => { const c = el.querySelector(':scope > figcaption'); if (c) c.style.display = 'none'; });
    const png = await f.screenshot({ type: 'png' });
    await f.evaluate((el, u) => {
      const c = el.querySelector(':scope > figcaption'), img = document.createElement('img');
      img.src = u; img.alt = c ? c.textContent : ''; el.replaceChildren(img);
      if (c) { c.style.display = ''; el.append(c); }
    }, 'data:image/png;base64,' + png.toString('base64'));
  }
  require('fs').writeFileSync(out, await pg.content());
  await b.close();
})();
