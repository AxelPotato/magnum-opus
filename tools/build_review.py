"""Build the review copy of the essay: all four parts on one page, for the shared Artifact.

    python tools/build_review.py OUT.html

Run it on a checkout of main. It builds each part with essay/build_html.py (the same text,
figures and styles as the essay pages), puts the four parts behind the essay's own part tabs,
prefixes every id with its part so the parts can share one page, adds a "Comment on this part"
button for readers who can comment, and turns the contact form into a note, because an
Artifact cannot reach the form's webhook. It writes only OUT.html: not part of the release flow.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'essay'))
import build_html as B  # noqa: E402

TABS = ['intro', 'rational', 'spiritual', 'practical']
NEXT = ['Part one: Rational', 'Part two: Spiritual', 'Part three: Practical']

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
"""

REVIEW_JS = """
(function () {
  var parts = [].slice.call(document.querySelectorAll('.part'));
  var names = %s;
  function show(i) {
    parts.forEach(function (p, k) { p.hidden = k !== i; });
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

  var buttons = [].slice.call(document.querySelectorAll('.comment-part'));
  if (!window.claude || !window.claude.use) return;
  window.claude.use('comments').then(function (c) {
    if (!c) return;
    buttons.forEach(function (b) {
      b.hidden = false;
      b.addEventListener('click', function () {
        var h1 = b.closest('.part').querySelector('h1');
        c.openComposer({ element: h1 }).catch(function (err) {
          if (err && err.code === 'unavailable') buttons.forEach(function (x) { x.hidden = true; });
        });
      });
    });
  }, function () {});
})();
"""


def part_body(n):
    frag = B.page(n, fragment=True)
    body = frag[frag.index('<header class="hero">'):]
    body = body.replace(f'<script>{B.CONTACT_JS}</script>', '')
    body = re.sub(r' data-endpoint="[^"]*"', '', body)
    p = f'p{n}-'
    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{p}{m[1]}"', body)
    body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m[1]}"', body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m[1]})', body)
    # The essay's own part list becomes the tabs.
    names = ['Intro', 'Rational', 'Spiritual', 'Practical']
    for i, name in enumerate(names):
        if i != n:
            body = body.replace(f'<li>{name}</li>', f'<li><a href="#{TABS[i]}">{name}</a></li>', 1)
    end = '<div class="part-end" data-uncommentable>'
    if n < 3:
        end += f'<a href="#{TABS[n + 1]}">Next: {html.escape(NEXT[n])}</a>'
    end += '<button type="button" class="comment-part" hidden>Comment on this part</button>'
    end += '</div>'
    body = body.replace('<footer>', end + '<footer>', 1)
    hidden = '' if n == 0 else ' hidden'
    return f'<section class="part" data-i="{n}" id="{TABS[n]}"{hidden}>{body}</section>'


def build():
    ver = open(os.path.join(ROOT, 'VERSION'), encoding='utf-8').read().strip()
    extras = ''.join(dict.fromkeys(B.PARTS[n]['css_extra'] for n in range(4)))
    head = (f'<title>Alex\'s Essay Draft</title>'
            f'<meta name="essay-version" content="{ver}">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="{B.FONTS}">'
            f'<style>{B.CSS}{extras}{REVIEW_CSS}</style>'
            f'<script>{B.UTM_JS}</script>')
    bar = (f'<div class="review-bar" data-uncommentable><p>A draft, shared for feedback. Version {ver}. '
           'Notes on any paragraph are welcome.</p></div>')
    parts = ''.join(part_body(n) for n in range(4))
    return head + bar + parts + '<script>' + (REVIEW_JS % repr(TABS)) + '</script>'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = build()
    open(sys.argv[1], 'w', encoding='utf-8').write(text)
    print(sys.argv[1], round(len(text) / 1024), 'KB')
