"""The shelf of solutions from Part one's BE section, as a toy: pick an everyday problem, move one
slider from braced to released, and more books on the shelf light up. Four problems, four steps of
letting go, one short text for each of the sixteen.

widget() returns the whole figure (problem buttons, slider, shelves, texts and its script). Without
script the page shows the first problem at braced, which is the essay's own picture: one default
answer and a shelf ruled out. Imported by build_html.py.
"""

CSS_EXTRA = r"""
.shelf [hidden]{display:none!important}
.shelf .lead{font-family:var(--mono);font-size:.78rem;line-height:1.5;color:var(--muted);text-align:center;margin:0 auto .5rem;max-width:34rem}
.shelf .hint{font-family:var(--mono);font-size:.72rem;color:var(--muted);text-align:center;margin:0 0 .5rem}
.shelf .probs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.4rem;margin:0 auto .9rem;max-width:40rem}
.shelf .probs button{font-family:var(--mono);font-size:.74rem;line-height:1.35;text-align:left;color:var(--ink);background:transparent;border:0;border-top:1.5px solid var(--rule);border-radius:0;padding:.5rem .2rem .45rem;cursor:pointer;transition:border-color .2s,color .2s}
.shelf .probs button:hover{border-top-color:var(--drifting)}
.shelf .probs button[aria-pressed="true"]{border-top:3px solid var(--drifting);color:var(--drifting);font-weight:600;padding-top:.4rem}
.shelf .probs button:focus-visible,.shelf input:focus-visible{outline:2px solid var(--drifting);outline-offset:2px}
.shelf .prob{display:none}
.shelf .prob.on{display:block}
.shelf .books{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:.4rem;max-width:44rem;margin:0 auto;padding:0 .2rem .35rem;border-bottom:3px solid var(--ink)}
.shelf .bk{min-height:7.2rem;border-radius:6px;padding:.5rem .35rem;display:flex;align-items:center;justify-content:center;text-align:center;
  font-family:var(--mono);font-size:.7rem;line-height:1.35;color:var(--muted);hyphens:none;overflow-wrap:break-word;border:1.5px dashed var(--muted);transition:background .35s,border-color .35s,color .35s}
.shelf .bk .ans{display:none;color:var(--ink)}
.shelf .bk.lit{border:2px solid var(--drifting);background:color-mix(in srgb,var(--drifting) 13%,var(--card));animation:shelfin .4s ease}
.shelf .bk.lit .ans{display:inline}.shelf .bk.lit .cat{display:none}
.shelf .bk.dflt{border:2.2px solid var(--high);background:color-mix(in srgb,var(--high) 16%,var(--card))}
@keyframes shelfin{from{transform:translateY(5px)}to{transform:none}}
.shelf .count{font-family:var(--mono);font-size:.74rem;color:var(--muted);text-align:center;margin:.5rem 0 0}
.shelf .be{display:flex;align-items:center;gap:.7rem;max-width:30rem;margin:0 auto;padding:0 .5rem}
.shelf .be span{font-family:var(--mono);font-size:.72rem;color:var(--muted);white-space:nowrap}
.shelf .be input{flex:1;min-width:0;accent-color:var(--drifting);cursor:pointer}
.shelf .lvl{font-family:var(--mono);font-size:.78rem;font-weight:600;color:var(--drifting);text-align:center;margin:.2rem 0 .9rem}
.shelf .say{max-width:34rem;margin:.9rem auto 0;text-align:left}
.shelf .say p{font-size:1rem;line-height:1.55;margin:0;display:none}
.shelf .say p.on{display:block;animation:shelfin .35s ease}
@media (max-width:620px){.shelf .probs{grid-template-columns:1fr;gap:0}.shelf .books{grid-template-columns:repeat(4,minmax(0,1fr))}.shelf .bk{min-height:6rem}}
@media (prefers-reduced-motion:reduce){.shelf .bk,.shelf .bk.lit,.shelf .say p.on{animation:none;transition:none}}
"""

# the four steps of the slider, from braced to released
LEVELS = ['braced', 'a little looser', 'fairly loose', 'released']

# what a ruled-out book says on its spine, by the step that lights it
CATS = ['', 'unusual', 'embarrassing', 'kind of crazy']

# each problem: button label, the default answer, six more answers (two per step, steps 1 to 3),
# and one text per step (0 to 3)
PROBLEMS = [
    dict(label='The dog next door barks all night',
         default='Earplugs, and a sigh',
         more=['Leave a polite note', 'Ask the other neighbors if they hear it too',
               'Knock and just ask', 'Ask if the dog is home alone all evening',
               'Offer to walk the dog', 'Bring cookies and admit you’ve been angry for a month'],
         say=["You took the only book you could see, and the dog keeps barking.",
              "A note is safe, because nobody has to see your face.",
              "A little embarrassing, and quite often the neighbor had no idea.",
              "Walking the dog sounds crazy, and then the dog gets tired and you get to sleep."]),
    dict(label='A colleague presents your idea as theirs',
         default='Say nothing, and stew for a week',
         more=['Vent to a friend over lunch', 'Mention it, very casually, in the next meeting',
               'Ask them for coffee and say how it felt', 'Tell your manager calmly that it was yours',
               'Ask them to build the next one with you', 'Admit you’ve done it to someone too'],
         say=["By Friday you have rehearsed eleven speeches and given none of them.",
              "The casual mention is a speech wearing a disguise.",
              "Saying how it felt, without a verdict, beats all eleven speeches.",
              "Building the next one together turns a rival into a teammate."]),
    dict(label='The group chat goes quiet after your message',
         default='Reread it ten times',
         more=['Send a funny sticker to cover it', 'Ask one friend privately if it was weird',
               'Assume they’re busy, because they probably are', 'Put the phone down and get on with your day',
               'Write “well, that landed”', 'Call the one friend you actually wanted to talk to'],
         say=["It was a message about Saturday.",
              "You’re still in the meeting that isn’t happening, just with company now.",
              "Most people are making dinner or driving home.",
              "Laughing at yourself weighs a lot less than ten rereads."]),
    dict(label='You haven’t called your sister in a year',
         default='Wait for her to call first',
         more=['Like her photos so she knows you’re alive', 'Ask your mom how she’s doing',
               'Send “thinking of you” and nothing else', 'Call, and talk about the weather',
               'Call and say you miss her', 'Say sorry first, even if it was half hers'],
         say=["She is probably waiting for you to call first, too.",
              "Contact through a side door, so nobody has to say anything.",
              "Awkward for a minute, and then it’s just your sister.",
              "The sorry is the heaviest book on the shelf, and the one that ends the year."]),
]

START = (0, 0)  # first problem, braced: the essay's own picture


def books(p):
    out = [f'<div class="bk dflt lit" data-l="0"><span class="ans">{p["default"]}</span></div>']
    for i, a in enumerate(p['more']):
        step = i // 2 + 1
        out.append(f'<div class="bk" data-l="{step}"><span class="cat">{CATS[step]}</span><span class="ans">{a}</span></div>')
    return ''.join(out)


JS = r"""
(function(){
  document.querySelectorAll('.shelf').forEach(function(f){
    var p=0, l=0, rng=f.querySelector('input'), lv=f.querySelector('.lvl'), names=%LEVELS%;
    function draw(){
      f.querySelectorAll('.probs button').forEach(function(b,i){b.setAttribute('aria-pressed',i===p?'true':'false');});
      f.querySelectorAll('.prob').forEach(function(d,i){d.classList.toggle('on',i===p);});
      var lit=0, all=0;
      f.querySelectorAll('.prob.on .bk').forEach(function(b){var on=+b.getAttribute('data-l')<=l; b.classList.toggle('lit',on); all++; if(on) lit++;});
      f.querySelectorAll('.prob.on .say p').forEach(function(s,i){s.classList.toggle('on',i===l);});
      var out=all-lit;
      f.querySelector('.prob.on .count').textContent= out ? out+' of '+all+' ruled out before you noticed you were deciding' : 'Nothing ruled out. You still have to pick one.';
      lv.textContent=names[l]; rng.setAttribute('aria-valuetext',names[l]);
    }
    f.querySelectorAll('.probs button').forEach(function(b,i){b.addEventListener('click',function(){p=i; draw();});});
    rng.addEventListener('input',function(){l=+rng.value; draw();});
    f.querySelector('.probs').hidden=false; f.querySelector('.be').hidden=false; f.querySelector('.hint').hidden=false; lv.hidden=false;
    draw();
  });
})();
"""


def widget(caption='The shelf of solutions for one everyday problem, and how much of it you can see.'):
    import json
    p0, l0 = START
    btns = ''.join(f'<button type="button" aria-pressed="{"true" if i == p0 else "false"}">{p["label"]}</button>'
                   for i, p in enumerate(PROBLEMS))
    probs = []
    for i, p in enumerate(PROBLEMS):
        on = ' on' if i == p0 else ''
        says = ''.join(f'<p class="{"on" if (i == p0 and j == l0) else ""}">{s}</p>' for j, s in enumerate(p['say']))
        probs.append(f'<div class="prob{on}"><div class="books">{books(p)}</div>'
                     f'<p class="count">6 of 7 ruled out before you noticed you were deciding</p>'
                     f'<div class="say" aria-live="polite">{says}</div></div>')
    return (f'<figure class="fig shelf">'
            f'<p class="lead">{caption}</p>'
            f'<p class="hint" hidden>Pick a problem, then let go one step at a time.</p>'
            f'<div class="probs" hidden>{btns}</div>'
            f'<div class="be" hidden><span>BE</span><input type="range" id="shelf-be" min="0" max="3" step="1" value="{l0}" '
            f'aria-label="BE, from braced to released"><span>released</span></div>'
            f'<p class="lvl" hidden>{LEVELS[l0]}</p>'
            f'{"".join(probs)}'
            f'<script>{JS.replace("%LEVELS%", json.dumps(LEVELS))}</script></figure>')
