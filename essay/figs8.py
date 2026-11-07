"""Two ladders for Part one, after "The line": DO and BE, five steps each, as two sliders. Pick a part
of life, move either ladder, and one line shows what that step looks like there. A small cross puts a
dot on the chart, and a third line reads the pair by its distance from the line of harmony.

widget() returns the whole figure. Without script the page shows the start state (I keep my word,
braced, at work), which sits below the line, in Driven. Imported by build_html.py.
"""
import json

CSS_EXTRA = r"""
.ladders [hidden]{display:none!important}
.ladders .lead{font-family:var(--mono);font-size:.78rem;line-height:1.5;color:var(--muted);text-align:center;margin:0 auto .5rem;max-width:34rem}
.ladders .hint{font-family:var(--mono);font-size:.72rem;color:var(--muted);text-align:center;margin:0 0 .5rem}
.ladders .areas{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;margin:0 auto 1rem;max-width:36rem;border:1.5px solid var(--high);border-radius:6px;overflow:hidden}
.ladders .areas button{font-family:var(--mono);font-size:.74rem;line-height:1.35;text-align:center;color:var(--high);background:var(--card);border:0;border-left:1.5px solid var(--high);border-radius:0;padding:.6rem .4rem;cursor:pointer;transition:background .2s,color .2s}
.ladders .areas button:first-child{border-left:0}
.ladders .areas button:hover{background:color-mix(in srgb,var(--high) 12%,var(--card))}
.ladders .areas button[aria-pressed="true"]{background:var(--high);color:var(--paper);font-weight:600}
.ladders button:focus-visible,.ladders input:focus-visible{outline:2px solid var(--high);outline-offset:2px}
.ladders .hy{display:grid;grid-template-columns:minmax(0,1fr) 7.5rem;gap:1.2rem;align-items:center;max-width:36rem;margin:0 auto}
.ladders .sl{display:flex;flex-direction:column;gap:.8rem;min-width:0}
.ladders .row{display:grid;grid-template-columns:2.2rem minmax(0,1fr);gap:.1rem .6rem;align-items:center}
.ladders .row b{font-family:var(--mono);font-size:.78rem;font-weight:600;grid-row:span 2}
.ladders .row input{width:100%;min-width:0;cursor:pointer;margin:0}
.ladders .row .w{font-family:var(--mono);font-size:.74rem;font-weight:600;grid-column:2}
.ladders .row.do b,.ladders .row.do .w{color:var(--driven)}.ladders .row.do input{accent-color:var(--driven)}
.ladders .row.be b,.ladders .row.be .w{color:var(--drifting)}.ladders .row.be input{accent-color:var(--drifting)}
.ladders .cross{width:100%;height:auto;display:block}
.ladders .cross circle{transition:cx .3s ease,cy .3s ease}
.ladders .lines{max-width:34rem;margin:1rem auto 0;display:flex;flex-direction:column;gap:.7rem;text-align:left}
.ladders .lines p{margin:0;padding-left:.8rem;border-left:3px solid var(--c);font-size:1rem;line-height:1.55}
.ladders .lines .tag{display:block;font-family:var(--mono);font-size:.7rem;color:var(--muted);line-height:1.4}
@media (max-width:620px){.ladders .areas{grid-template-columns:1fr}.ladders .areas button{border-left:0;border-top:1.5px solid var(--high)}.ladders .areas button:first-child{border-top:0}.ladders .hy{grid-template-columns:minmax(0,1fr) 5.5rem;gap:.8rem}}
@media (prefers-reduced-motion:reduce){.ladders .cross circle{transition:none}}
"""

AREAS = ['At work', 'With people close to you', 'Alone with yourself']

# each step: its name, then one line per area (work, people, alone)
DO = [
    ('it happens to me', ['You do what lands on your desk, and complain about what lands on your desk.',
                          'You wait to be invited, and wonder why nobody calls.',
                          'The evening goes wherever the phone takes it.']),
    ('I react', ['You answer fast and put out every fire, and somehow the week is gone.',
                 'You say yes when someone asks, and you show up.',
                 'You plan the day and follow about half of it.']),
    ('I keep my word', ['What you promised on Monday is done by Friday.',
                        'When you say you’ll call on Sunday, the phone rings on Sunday.',
                        'The form you’ve been avoiding is filled in by lunch.']),
    ('I start things', ['You fix the thing nobody owns, without being asked.',
                        'You’re the one who gets everybody together, and they know it.',
                        'You sign up for the class instead of saving the link.']),
    ('I make it happen', ['There is a project that wouldn’t exist without you, and other people grow inside it.',
                          'Things happen for the people around you, too, because you moved first.',
                          'The big dream gets today’s small step, every day.']),
]

BE = [
    ('braced', ['Before the meeting you’ve already rehearsed three ways it could go wrong.',
                'You never say sorry first. They started it, after all.',
                'Your body is on the couch and your mind is in yesterday’s argument.']),
    ('noticing', ['In the meeting you feel your jaw clench, and that’s new.',
                  'You say sorry a day late, and it still counts.',
                  'You catch yourself replaying the argument and stop for a minute.']),
    ('taking the first step', ['You say “I was wrong about that” in front of everyone.',
                               'You send the first message after the long silence.',
                               'You sit for five minutes without reaching for the phone.']),
    ('at ease', ['Criticism stings, and it’s gone by lunch.',
                 'You can tell someone you’re hurt while you’re still hurt, and calmly.',
                 'A feeling arrives and you notice it while it’s happening.']),
    ('released', ['The odd idea stops feeling dangerous, so you finally say it.',
                  'You tell a friend you’re proud of them, and you take a compliment without arguing.',
                  'A slow evening on your own feels like plenty.']),
]

# the pair, by DO minus BE: 0 on the line, 1 and 2+ below it (Driven side), -1 and -2 or less above it
PAIR = {
    0: 'In step. What you want inside and what you do outside move together, and from here you can climb along the line.',
    1: 'The doing is a step ahead. Easing off a little would let the inside catch up.',
    2: 'This is Driven. Things get done, and the tension comes along to every one of them.',
    -1: 'The inside is a step ahead. One plan for tomorrow, kept, would close the gap.',
    -2: 'This is Drifting. A lot of peace inside, and not much changes around you.',
}

START = (0, 2, 0)  # at work, I keep my word, braced: below the line, the most common picture


def pair(d, b):
    g = max(-2, min(2, d - b))
    return PAIR[g]


def _xy(d, b):
    return 12 + d * 19, 88 - b * 19


JS = r"""
(function(){
  document.querySelectorAll('.ladders').forEach(function(f){
    var D=%DO%, B=%BE%, P=%PAIR%, a=%A0%;
    var rd=f.querySelector('.row.do input'), rb=f.querySelector('.row.be input'), dot=f.querySelector('.cross circle');
    function draw(){
      var d=+rd.value, b=+rb.value, g=Math.max(-2,Math.min(2,d-b));
      f.querySelectorAll('.areas button').forEach(function(x,i){x.setAttribute('aria-pressed',i===a?'true':'false');});
      f.querySelector('.row.do .w').textContent=D[d][0]; rd.setAttribute('aria-valuetext',D[d][0]);
      f.querySelector('.row.be .w').textContent=B[b][0]; rb.setAttribute('aria-valuetext',B[b][0]);
      f.querySelector('.say-do').textContent=D[d][1][a];
      f.querySelector('.say-be').textContent=B[b][1][a];
      f.querySelector('.say-pair').textContent=P[g];
      dot.setAttribute('cx',12+d*19); dot.setAttribute('cy',88-b*19);
    }
    f.querySelectorAll('.areas button').forEach(function(x,i){x.addEventListener('click',function(){a=i; draw();});});
    rd.addEventListener('input',draw); rb.addEventListener('input',draw);
    f.querySelector('.areas').hidden=false; f.querySelector('.sl').hidden=false; f.querySelector('.hint').hidden=false;
    draw();
  });
})();
"""


def widget(caption='Two ladders, DO and BE, five steps each, and what each step looks like in one part of life.'):
    a0, d0, b0 = START
    x, y = _xy(d0, b0)
    btns = ''.join(f'<button type="button" aria-pressed="{"true" if i == a0 else "false"}">{t}</button>'
                   for i, t in enumerate(AREAS))
    cross = ('<svg class="cross" viewBox="0 0 100 100" role="img" aria-label="The cross with the line of harmony and a dot for the two ladders">'
             '<rect x="6" y="6" width="88" height="88" fill="none" stroke="var(--rule)" stroke-width="1.2"/>'
             '<line x1="50" y1="6" x2="50" y2="94" stroke="var(--rule)" stroke-width="1"/>'
             '<line x1="6" y1="50" x2="94" y2="50" stroke="var(--rule)" stroke-width="1"/>'
             '<line x1="6" y1="94" x2="94" y2="6" stroke="var(--high)" stroke-width="1.6" stroke-dasharray="3 3"/>'
             f'<circle cx="{x}" cy="{y}" r="5.5" fill="var(--ink)"/></svg>')
    rows = (f'<div class="sl" hidden>'
            f'<div class="row do"><b>DO</b><input type="range" id="ladder-do" min="0" max="4" step="1" value="{d0}" '
            f'aria-label="DO, from it happens to me to I make it happen"><span class="w">{DO[d0][0]}</span></div>'
            f'<div class="row be"><b>BE</b><input type="range" id="ladder-be" min="0" max="4" step="1" value="{b0}" '
            f'aria-label="BE, from braced to released"><span class="w">{BE[b0][0]}</span></div></div>')
    lines = (f'<div class="lines" aria-live="polite">'
             f'<p style="--c:var(--driven)"><span class="tag">what you do</span><span class="say-do">{DO[d0][1][a0]}</span></p>'
             f'<p style="--c:var(--drifting)"><span class="tag">how you are inside</span><span class="say-be">{BE[b0][1][a0]}</span></p>'
             f'<p style="--c:var(--high)"><span class="tag">the two together</span><span class="say-pair">{pair(d0, b0)}</span></p></div>')
    js = (JS.replace('%DO%', json.dumps([[n, t] for n, t in DO], ensure_ascii=False))
            .replace('%BE%', json.dumps([[n, t] for n, t in BE], ensure_ascii=False))
            .replace('%PAIR%', json.dumps({str(k): v for k, v in PAIR.items()}, ensure_ascii=False))
            .replace('%A0%', str(a0)))
    return (f'<figure class="fig ladders">'
            f'<p class="lead">{caption}</p>'
            f'<p class="hint" hidden>Pick a part of life, then move one ladder a step at a time.</p>'
            f'<div class="areas" hidden>{btns}</div>'
            f'<div class="hy">{rows}{cross}</div>'
            f'{lines}'
            f'<script>{js}</script></figure>')
