#!/usr/bin/env python3
"""Build the downloadable book, a PDF and an EPUB, from the same part files as the website.

    python tools/build_book.py        # writes essay/book/rational-spiritual-practical.pdf and .epub

Needs Node with Playwright and Chromium (tools/book_render.js prints the PDF and draws the figures as
pictures for the EPUB) and pandoc (for the EPUB). release.py runs it after every release; if a tool is missing it says so
and the old files stay. Kindle takes EPUB through Send to Kindle, so there is no separate Kindle file.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ESSAY = os.path.join(ROOT, 'essay')
OUT = os.path.join(ESSAY, 'book')
sys.path.insert(0, ESSAY)
import build_html as B  # noqa: E402

NAME = 'rational-spiritual-practical'

BOOK_CSS = r"""
:root{--paper:#FFFFFF;--card:#FFFFFF}
h2{break-inside:avoid}
body{font-size:1.06rem;line-height:1.62}
.titlepage{min-height:88vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;break-after:page}
.titlepage h1{font-size:3.4rem}
.titlepage .by{font-family:var(--head);font-style:italic;font-size:1.3rem;color:var(--muted);margin:1rem 0 0}
.titlepage .ver{font-family:var(--mono);font-size:.75rem;color:var(--muted);margin-top:3rem}
.contents{break-after:page;max-width:34rem;margin:0 auto;padding-top:3rem}
.contents h2::before{display:none}
.contents ol{list-style:none;padding:0;margin:0}
.contents li{margin:0 0 1rem}
.contents a{color:var(--ink);text-decoration:none;display:flex;flex-direction:column}
.contents a span{font-family:var(--mono);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.contents a b{font-family:var(--head);font-weight:600;font-size:1.25rem}
.chapter{break-before:page}
.chapter .hero{padding:4rem 0 1rem}
.col{margin-top:2rem}
.fold{margin:1.4rem 0;padding:.2rem 0 .2rem .9rem;border-left:2px solid var(--kc,var(--muted));break-inside:auto}
.fold.k-trad{--kc:var(--k-trad)}.fold.k-study{--kc:var(--k-study)}.fold.k-look{--kc:var(--k-look)}.fold.k-life{--kc:var(--k-life)}.fold.k-story{--kc:var(--k-story)}
.fold .fk{font-family:var(--mono);font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--kc);margin:0 0 .2rem}
.fold .ft{font-family:var(--head);font-weight:600;font-size:1.1rem;margin:0 0 .6rem;text-transform:none;letter-spacing:0;color:var(--ink)}
.fig{width:100%!important;left:0!important;transform:none!important;break-inside:avoid}
.fig .hint,.fig .bar,.fig .lead{display:none!important}
h2,h3{break-after:avoid}
p{orphans:3;widows:3}
a{color:inherit}
"""

def chapter(n):
    cfg = B.PARTS[n]
    md = open(os.path.join(ESSAY, cfg['md']), encoding='utf-8').read()
    body, _ = B.convert(md, cfg['rules']())
    hero = B.hero_html(n, B.reading_words(md)).replace('<p class="meta">', '<p class="meta" hidden>')
    cast = B.cast_html() if cfg['cast'] else ''
    return (f'<section class="chapter" id="ch{n}">' + hero + '<main><div class="col">' + cast + '\n'.join(body) + '</div></main></section>')


def book_html(ver):
    css = B.CSS + ''.join(B.PARTS[n]['css_extra'] for n in range(5)) + BOOK_CSS
    toc = ''.join(f'<li><a href="#ch{n}"><span>{B.NUMS[n]}</span><b>{B.HEADS[n]}</b></a></li>' for n in range(5))
    title = (f'<section class="titlepage"><p class="kicker">A short book</p><h1>{B.BOOK_TITLE}</h1>'
             f'<p class="by">by Alex</p><p class="ver">Version {ver}</p></section>'
             f'<nav class="contents"><h2>Contents</h2><ol>{toc}</ol></nav>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<title>{B.BOOK_TITLE}</title><link rel="stylesheet" href="{B.FONTS}"><style>{css}</style></head>'
            '<body>' + title + ''.join(chapter(n) for n in range(5)) + '</body></html>')


def main():
    ver = open(os.path.join(ROOT, 'VERSION')).read().strip()
    os.makedirs(OUT, exist_ok=True)
    src = os.path.join(OUT, '.book.html')
    epub_src = os.path.join(OUT, '.book-epub.html')
    open(src, 'w', encoding='utf-8').write(book_html(ver))
    subprocess.run(['node', os.path.join(ROOT, 'tools', 'book_render.js'), src, os.path.join(OUT, NAME + '.pdf'), epub_src], check=True)
    html = open(epub_src, encoding='utf-8').read()
    # The EPUB keeps the text, the pictures and the chapter headings; colors and layout are the reader's.
    html = re.sub(r'<svg class="ki".*?</svg>', '', html, flags=re.S)
    html = re.sub(r'<(header|main|section|div)[^>]*>|</(header|main|section|div)>', '', html)
    html = re.sub(r'<p class="kicker">([^<]*)</p>\s*<h1>([^<]*)</h1>', r'<h1>\1: \2</h1>', html)
    html = re.sub(r'<nav class="contents">.*?</nav>', '', html, flags=re.S)
    html = re.sub(r'<h1>A short book: [^<]*</h1>.*?(?=<h1>)', '', html, count=1, flags=re.S)
    html = re.sub(r'<style>.*?</style>|<link[^>]*>', '', html, flags=re.S)
    open(epub_src, 'w', encoding='utf-8').write(html)
    css = os.path.join(OUT, '.epub.css')
    open(css, 'w').write('body{font-family:serif;line-height:1.5}h1{margin-top:2em}.kicker,.fk{font-size:.8em;text-transform:uppercase;letter-spacing:.08em}'
                         '.lede{font-style:italic}img{max-width:100%}figure{margin:1.2em 0;text-align:center}figcaption{font-size:.85em;font-style:italic}'
                         '.fold{border-left:2px solid #999;padding-left:.8em;margin:1em 0}.ft{font-size:1em;margin:.2em 0 .5em}.who{display:inline-block;width:5em;margin:0 .6em .4em 0;text-align:center;font-size:.75em}'
                         '.who img{width:4.5em;height:4.5em;border-radius:50%}.meta,.orn{display:none}')
    subprocess.run(['pandoc', epub_src, '-f', 'html', '-o', os.path.join(OUT, NAME + '.epub'), '--split-level=1', '--toc', '--toc-depth=2',
                    '--css', css, '--metadata', f'title={B.BOOK_TITLE}', '--metadata', 'author=Alex', '--metadata', 'lang=en-US',
                    '--metadata', f'subtitle=Version {ver}'], check=True)
    for f in (src, epub_src, css):
        os.remove(f)
    for f in ('pdf', 'epub'):
        print(os.path.join(OUT, f'{NAME}.{f}'), round(os.path.getsize(os.path.join(OUT, f'{NAME}.{f}')) / 1024), 'KB')


if __name__ == '__main__':
    main()
