"""Build the review copy of the essay: all four parts and the Next page on one page, for the shared Artifact.

    python tools/build_review.py OUT.html

Run it on a checkout of main. It builds each part with essay/build_html.py (the same text,
figures and styles as the essay pages), puts the pages behind the essay's own tabs,
and prefixes every id with its part so the parts can share one page. The open part's contents
list is a left sidebar on wide screens and a hamburger drawer on phones, as on the essay pages. Readers who can comment
get a "Comment on this part" button and can select any words or tap a paragraph, then press
Comment. The contact form on the Next page turns into a note, because an Artifact cannot reach its webhook.
It writes only OUT.html: not part of the release flow.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'essay'))
import build_html as B  # noqa: E402

TABS = ['intro', 'rational', 'spiritual', 'practical', 'next']
NEXT = ['Part one: Rational', 'Part two: Spiritual', 'Part three: Practical', 'leave your details']

REVIEW_CSS = """
.review-bar{background:var(--card);border-bottom:1px solid var(--rule);font-family:var(--mono);font-size:.78rem;line-height:1.5;color:var(--muted);padding:.6rem 1rem}
.review-bar p{max-width:40rem;margin:0 auto}
.parts a{color:inherit;text-decoration:none}
.parts a:focus-visible,.part-end a:focus-visible,.part-end button:focus-visible{outline:2px solid var(--drifting);outline-offset:3px}
.parts li:has(a):hover{border-color:var(--ink);color:var(--ink)}
.part-end{max-width:40rem;margin:3rem auto 2rem;display:flex;flex-wrap:wrap;gap:.75rem;align-items:center}
.part-end a,.part-end button{font-family:var(--mono);font-size:.85rem;padding:.55rem 1rem;border-radius:999px;border:1px solid var(--ink);cursor:pointer;text-decoration:none}
.part-end a{background:var(--ink);color:var(--paper)}
.part-end button{background:transparent;color:var(--ink)}
.part-end .note{flex-basis:100%;margin:0;font-family:var(--mono);font-size:.78rem;color:var(--muted)}
.part main .marked{background:color-mix(in srgb,var(--drifting) 16%,transparent);box-shadow:0 0 0 .35rem color-mix(in srgb,var(--drifting) 16%,transparent);border-radius:3px}
@media (hover:hover){.marking .part main :is(p,li,figure,h2,h3,h4):not(.marked):hover{background:color-mix(in srgb,var(--drifting) 6%,transparent);box-shadow:0 0 0 .35rem color-mix(in srgb,var(--drifting) 6%,transparent);border-radius:3px}}
#comment-pop{position:absolute;z-index:20;font-family:var(--mono);font-size:.82rem;padding:.45rem .95rem;border-radius:999px;border:0;background:var(--ink);color:var(--paper);cursor:pointer;box-shadow:0 2px 12px color-mix(in srgb,var(--ink) 25%,transparent)}
#comment-pop:focus-visible{outline:2px solid var(--drifting);outline-offset:3px}
@media (max-width:72rem){body.has-toc .review-bar{padding-left:4rem}}
"""

REVIEW_JS = """
(function () {
  var parts = [].slice.call(document.querySelectorAll('.part'));
  var names = %s;
  var clearMark = function () {};

  // The open part's contents list: a left sidebar on wide screens, a hamburger drawer on narrow
  // ones, as on the essay pages. Parts without one (Next) get neither.
  var b = document.body, btn = document.querySelector('.toc-btn'), nav = null, links = [], heads = [], last = -2;
  function setOpen(o) { b.classList.toggle('toc-open', o); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); }
  function spy() {
    if (!nav) return;
    var y = window.innerHeight * 0.25, cur = -1;
    heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top <= y) cur = i; });
    if (cur === last) return;
    last = cur;
    links.forEach(function (a, i) { a.classList.toggle('on', i === cur); if (i === cur) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    if (cur >= 0) { var a = links[cur]; if (a.offsetTop < nav.scrollTop + 40 || a.offsetTop + a.offsetHeight > nav.scrollTop + nav.clientHeight - 40) nav.scrollTop = a.offsetTop - 80; }
  }
  function tocFor(p) {
    setOpen(false);
    nav = p.querySelector('nav.toc');
    b.classList.toggle('has-toc', !!nav);
    links = nav ? [].slice.call(nav.querySelectorAll('a')) : [];
    heads = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
    if (nav) btn.setAttribute('aria-controls', nav.id);
    last = -2;
    spy();
  }
  btn.addEventListener('click', function () { setOpen(!b.classList.contains('toc-open')); });
  document.querySelector('.toc-scrim').addEventListener('click', function () { setOpen(false); });
  document.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('.toc a')) setOpen(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  window.addEventListener('scroll', spy, { passive: true });

  function show(i) {
    clearMark();
    parts.forEach(function (p, k) { p.hidden = k !== i; });
    tocFor(parts[i]);
    try { localStorage.setItem('essay_review_tab', String(i)); } catch (e) {}
  }
  function setHash(h) { try { history.replaceState(null, '', '#' + h); } catch (e) {} }
  function go(h, smooth) {
    var i = names.indexOf(h);
    if (i >= 0) { show(i); window.scrollTo(0, 0); return true; }
    var el = h && document.getElementById(h);
    if (!el) return false;
    show(+el.closest('.part').dataset.i);
    var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    el.scrollIntoView({ behavior: smooth && !calm ? 'smooth' : 'auto' });
    return true;
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    var h = a.getAttribute('href').slice(1);
    if (go(h, names.indexOf(h) < 0)) { e.preventDefault(); setHash(h); }
  });
  window.addEventListener('hashchange', function () { go(location.hash.slice(1), false); });
  var start = location.hash.slice(1), saved = null;
  try { saved = localStorage.getItem('essay_review_tab'); } catch (e) {}
  if (!go(start, false)) show(saved !== null && parts[+saved] ? +saved : 0);

  // Comment-mode clicks inside a paragraph anchor to the whole paragraph.
  document.querySelectorAll('.part main p, .part main li, .part main figure, .part h1').forEach(function (el) {
    el.setAttribute('data-comment-target', '');
  });

  // The contact form cannot reach its webhook from an Artifact, so it says so instead of sending.
  document.querySelectorAll('.contact-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      f.querySelector('.contact-status').textContent = 'This is a review copy, so the form does not send anything here. On the real page it goes straight to Alex. If you would have sent it, a comment saying so helps a lot.';
    });
  });

  // Commenting: select any words, or tap a paragraph, then press Comment. The shell's own
  // composer opens on that spot. Shown only to readers this page can open a composer for.
  var buttons = [].slice.call(document.querySelectorAll('.comment-part'));
  function enableComments(c) {
    var off = false;
    var BLOCKS = 'p, li, figure, h2, h3, h4';
    var pop = document.createElement('button');
    pop.type = 'button';
    pop.id = 'comment-pop';
    pop.textContent = 'Comment';
    pop.hidden = true;
    pop.setAttribute('data-uncommentable', '');
    document.body.appendChild(pop);
    var target = null, marked = null, timer = null;
    function clear() {
      if (marked) marked.classList.remove('marked');
      marked = null; target = null; pop.hidden = true;
    }
    clearMark = clear;
    function disable() {
      off = true; clear();
      document.documentElement.classList.remove('marking');
      buttons.forEach(function (x) { x.hidden = true; });
      var how = document.querySelector('.review-bar .how');
      if (how) how.textContent = how.dataset.plain;
    }
    function place(rect) {
      pop.hidden = false;
      var w = pop.offsetWidth, vw = document.documentElement.clientWidth;
      var x = Math.min(Math.max(8, rect.right - w), vw - w - 8);
      pop.style.left = (x + window.scrollX) + 'px';
      var h = pop.offsetHeight;
      var y = rect.bottom + 8 + h > window.innerHeight ? rect.top - h - 8 : rect.bottom + 8;
      pop.style.top = (y + window.scrollY) + 'px';
    }
    function inEssay(node) {
      var el = node && (node.nodeType === 1 ? node : node.parentElement);
      return !!(el && el.closest('.part main') && !el.closest('[data-uncommentable], .contact, .toc'));
    }
    function fromSelection() {
      if (off) return false;
      var s = window.getSelection();
      if (!s || s.isCollapsed || !s.rangeCount || !String(s).trim()) return false;
      var r = s.getRangeAt(0);
      if (!inEssay(r.commonAncestorContainer)) return false;
      if (marked) marked.classList.remove('marked');
      marked = null;
      target = { range: r.cloneRange() };
      var rects = r.getClientRects();
      place(rects.length ? rects[rects.length - 1] : r.getBoundingClientRect());
      return true;
    }
    document.addEventListener('selectionchange', function () {
      clearTimeout(timer);
      timer = setTimeout(fromSelection, 350);
    });
    document.addEventListener('click', function (e) {
      if (off || e.target === pop) return;
      var s = window.getSelection();
      if (s && !s.isCollapsed && String(s).trim()) return;
      var el = e.target.closest && e.target.closest(BLOCKS);
      if (!el || !inEssay(el) || e.target.closest('a, button, input, textarea, select, summary, label')) { clear(); return; }
      if (el === marked) { clear(); return; }
      clear();
      marked = el;
      el.classList.add('marked');
      target = { element: el };
      // Next to the tap, so the button is on screen even for a long paragraph.
      place({ right: e.clientX + 48, top: e.clientY - 16, bottom: e.clientY + 16 });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') clear(); });
    window.addEventListener('resize', clear);
    pop.addEventListener('mousedown', function (e) { e.preventDefault(); });
    pop.addEventListener('click', function () {
      var t = target;
      if (!t) return;
      c.openComposer(t).then(function () {
        clear();
        try { window.getSelection().removeAllRanges(); } catch (x) {}
      }, function (err) {
        if (err && err.code === 'unavailable') disable();
      });
    });
    buttons.forEach(function (b) {
      b.hidden = false;
      b.addEventListener('click', function () {
        var h1 = b.closest('.part').querySelector('h1');
        c.openComposer({ element: h1 }).catch(function (err) {
          if (err && err.code === 'unavailable') disable();
        });
      });
    });
    document.documentElement.classList.add('marking');
    var how = document.querySelector('.review-bar .how');
    if (how) how.textContent = 'To comment, select any words or tap a paragraph, then press Comment.';
  }
  if (!window.claude || !window.claude.use) return;
  window.claude.use('comments').then(function (c) { if (c) enableComments(c); }, function () {});
})();
"""


def part_body(n):
    frag = B.page(n, fragment=True)
    body = frag[frag.index('<header class="hero">'):]
    body = body.replace(f'<script>{B.CONTACT_JS}</script>', '')
    body = re.sub(r' data-endpoint="[^"]*"', '', body)
    p = f'p{n}-'
    body = body.replace('<nav class="toc"', '<nav class="toc" id="toc"', 1)
    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{p}{m[1]}"', body)
    body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m[1]}"', body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m[1]})', body)
    # The essay's own part list becomes the tabs.
    for i, name in enumerate(B.NAMES):
        if i != n:
            body = body.replace(f'<li>{name}</li>', f'<li><a href="#{TABS[i]}">{name}</a></li>', 1)
    end = '<div class="part-end" data-uncommentable>'
    if n < len(TABS) - 1:
        end += f'<a href="#{TABS[n + 1]}">Next: {html.escape(NEXT[n])}</a>'
    end += '<button type="button" class="comment-part" hidden>Comment on this part</button>'
    end += '</div>'
    body = body.replace('<footer>', end + '<footer>', 1)
    hidden = '' if n == 0 else ' hidden'
    return f'<section class="part" data-i="{n}" id="{TABS[n]}"{hidden}>{body}</section>'


def build():
    ver = open(os.path.join(ROOT, 'VERSION'), encoding='utf-8').read().strip()
    extras = ''.join(dict.fromkeys(B.PARTS[n]['css_extra'] for n in range(len(TABS))))
    head = (f'<title>Alex\'s Essay Draft</title>'
            f'<meta name="essay-version" content="{ver}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="{B.FONTS}">'
            f'<style>{B.CSS}{B.TOC_CSS}{extras}{REVIEW_CSS}</style>'
            f'<script>{B.UTM_JS}</script>')
    plain = 'Notes on any paragraph are welcome.'
    bar = (f'<div class="review-bar" data-uncommentable><p>A draft, shared for feedback. Version {ver}. '
           f'<span class="how" data-plain="{plain}">{plain}</span></p></div>')
    toc_btn = ('<button class="toc-btn" type="button" aria-label="Contents" aria-expanded="false" data-uncommentable>'
               '<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg></button>'
               '<div class="toc-scrim"></div>')
    parts = ''.join(part_body(n) for n in range(len(TABS)))
    return head + bar + toc_btn + parts + '<script>' + (REVIEW_JS % repr(TABS)) + '</script>'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = build()
    open(sys.argv[1], 'w', encoding='utf-8').write(text)
    print(sys.argv[1], round(len(text) / 1024), 'KB')
