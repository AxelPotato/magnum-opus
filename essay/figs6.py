"""The four settings from Part two, step 2, as a toy: tap a slider to flip it between low and high,
and the picture and the short text under it change. Sixteen combinations, one drawing and one text each.

widget() returns the whole figure (sliders, sixteen scenes, sixteen texts and its script). Without
script the page shows the essay's own setup (know, do and last low, want high). Imported by build_html.py.
"""
from figs2 import T, person, svg

CSS_EXTRA = r"""
.toy{width:min(46rem,calc(100vw - 2rem))}
.toy .sliders{max-width:34rem}
.toy .sw{cursor:pointer;outline:none}
.toy .sw .knobf,.toy .sw .lvl{transition:transform .35s cubic-bezier(.5,1.6,.5,1)}
.toy .sw:focus-visible .slot{stroke:var(--high);stroke-width:3}
.toy .sw:hover .knobf{stroke:var(--high)}
.toy .sw .hit{fill:transparent}
.toy .scene{display:none}
.toy .scene.on{display:block;animation:toyin .35s ease}
@keyframes toyin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.toy .scene svg.chart{max-width:36rem}
.toy .say{max-width:34rem;margin:.6rem auto 0;text-align:left}
.toy .say h5{font-family:var(--display);font-weight:800;font-size:1.15rem;margin:.2rem 0 .3rem;color:var(--ink)}
.toy .say p{font-size:1rem;line-height:1.55;margin:0}
.toy .bar{display:flex;justify-content:center;gap:.6rem;flex-wrap:wrap;margin:.4rem 0 .2rem}
.toy .bar button{font-family:var(--mono);font-size:.75rem;color:var(--ink);background:var(--card);border:1.5px solid var(--rule);border-radius:999px;padding:.35rem .8rem;cursor:pointer}
.toy .bar button:hover{border-color:var(--high)}
.toy .lead{font-family:var(--mono);font-size:.78rem;line-height:1.5;color:var(--muted);text-align:center;margin:0 auto .2rem;max-width:34rem}
.toy .hint{font-family:var(--mono);font-size:.72rem;color:var(--muted);text-align:center;margin:.2rem 0 0}
.chart .catf{fill:var(--muted);fill-opacity:.35;stroke:var(--ink);stroke-width:2.2;stroke-linejoin:round}
.chart .sky{fill:#F2C14E;fill-opacity:.16;stroke:none}
.chart .fog{fill:var(--paper);fill-opacity:.82;stroke:none}
.chart .bolt{fill:#F2C14E;stroke:var(--ink);stroke-width:1.6;stroke-linejoin:round}
.chart .cloud{fill:var(--card);stroke:var(--rule);stroke-width:1.6}
"""

# order of the four sliders, and the words under each at low and at high
SETTINGS = [
    ('what it can know', 'a little', 'all of it'),
    ('what it can do', 'a little', 'anything'),
    ('how long it lasts', 'a little', 'forever'),
    ('what it wants', 'nothing', 'quite a lot'),
]
START = '0001'  # the setup the essay describes

TEXTS = {
    '0000': ('The cat on the windowsill',
             "It knows where the food is, it can reach most of it, its life is short and it wants very little beyond the warm spot by the window. "
             "Small world, big nap. This might be the most content setting on the page, and the cat is fully aware of it."),
    '0001': ('You and me, before coffee',
             "This is the setup from the paragraph above. It sees what is near, it reaches what is near, it has a birthday every year, "
             "and its wish list is longer than the calendar. Most of us live here, and it is where every good story starts."),
    '0010': ('The pebble on the beach',
             "It lasts practically forever and wants nothing at all. It doesn't know much and can't do much, and it is completely at peace with that. "
             "Great at meditation, a little weak on conversation."),
    '0011': ('The waiting room',
             "All the time in the world, a very clear idea of what it wants, no idea what is happening behind the door, and no way to make it go faster. "
             "Anyone who has spent an afternoon at a government office has visited this setting, and it felt like forever."),
    '0100': ('The strong friend on moving day',
             "Can lift anything you point at, has no idea where any of it goes, and is happy just to help. "
             "Wants a slice of pizza, maybe two, and is on the way home by evening. Every family needs one of these."),
    '0101': ('The teenager with the car keys',
             "Can do a lot, sees mostly what is right in front of the windshield, has one summer and wants everything in it. "
             "Most of us have been this setting once, and our parents remember it better than we do."),
    '0110': ('The river',
             "It takes its time, carves a canyon, never once looks at a map and wants nothing from anyone. "
             "Quietly the most productive thing on this page."),
    '0111': ('A god from the old myths',
             "Zeus, more or less. Powerful, immortal, wanting everything in sight, and somehow always the last to know what is going on in his own house. "
             "Read the Greek myths with this setting in mind and they turn into one long family sitcom."),
    '1000': ('The grandma on the porch',
             "She knows how it all works, she can no longer open the jar, and she wants nothing except for you to sit down and eat something. "
             "She has seen a lot of birthdays and stopped counting them a while ago."),
    '1001': ('The backseat driver',
             "Knows the best route, the right lane and the exact speed, can't touch the wheel, and wants very much to arrive before the shops close. "
             "Most of us have been this passenger, and the driver remembers every word."),
    '1010': ('The old library',
             "It holds the answer to almost anything, it can't fetch it for you, it will be there for centuries and it asks only for quiet. "
             "If you want something from it, you have to walk in yourself."),
    '1011': ('The statue in the park',
             "It has watched the town for generations, so it knows everyone's business. It can't move a finger and it will be standing there long after all of us, "
             "and it wants one thing very much, for the pigeon to leave."),
    '1100': ('The best plumber in town',
             "Knows what the noise is before you finish describing it, fixes it before the kettle boils, has another call after lunch, "
             "and wants nothing but a glass of water. A short visit that leaves everything working, which is a pretty good life plan."),
    '1101': ('The founder on a deadline',
             "Sees the whole market, can build almost anything, has until Friday, and wants the moon plus a little extra. "
             "Part one gave this one a room of its own."),
    '1110': ('The whole',
             "It knows everything, it can do anything, it has no clock and it wants nothing, because nothing is missing. Very peaceful, and a little short on plot. "
             "If you accept the axiom, that is exactly why the rest of this page exists."),
    '1111': ('The villain with the glove',
             "Knows everything, can do anything, lives forever, and still wants more. Thanos with the full glove, snapping his fingers and somehow still not satisfied. "
             "This one doesn't quite hold together, and that tells you something: a whole that lacks nothing has nothing left to want."),
}


# ------------------------------------------------------------------ small drawing helpers
def J(x, y, s, c='c2', anchor='start'):
    return T(x, y, s, f'dg2 {c}', anchor)


def ground(y=230, x0=40, x1=640):
    return f'<path class="stm" d="M{x0} {y} H{x1}"/>'


def think(x, y, w, h, lines, tail_x, tail_y, cls='small b'):
    """A thought bubble with its top-left at (x, y) and small circles trailing to (tail_x, tail_y)."""
    b = [f'<rect class="bubble" x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(h / 2, 22):.0f}"/>']
    mx, my = x + w / 2, y + h
    for t, r in ((0.3, 8), (0.62, 5.5), (0.88, 3.5)):
        cx = mx + (tail_x - mx) * t
        cy = my + (tail_y - my) * t
        b.append(f'<circle class="bubble" cx="{cx:.0f}" cy="{cy:.0f}" r="{r}"/>')
    step = (h - 16) / max(len(lines), 1)
    for i, s in enumerate(lines):
        b.append(T(x + w / 2, y + 18 + i * step + (step - 14) / 2 + 4, s, cls, 'middle'))
    return ''.join(b)


def say(x, y, w, h, s, tail_x, tail_y, c='c2'):
    """A speech bubble with a pointed tail to (tail_x, tail_y)."""
    mx = x + w / 2
    return (f'<path class="bubble" d="M{x + 12} {y} H{x + w - 12} Q{x + w} {y} {x + w} {y + 12} V{y + h - 12} Q{x + w} {y + h} {x + w - 12} {y + h} '
            f'H{mx + 14} L{tail_x} {tail_y} L{mx - 10} {y + h} H{x + 12} Q{x} {y + h} {x} {y + h - 12} V{y + 12} Q{x} {y} {x + 12} {y} Z"/>'
            + J(mx, y + h / 2 + 5, s, c, 'middle'))


def clock(x, y, r=16):
    return (f'<circle class="card" cx="{x}" cy="{y}" r="{r}"/>'
            f'<path class="st" d="M{x} {y} V{y - r * .6:.0f} M{x} {y} L{x + r * .45:.0f} {y + r * .2:.0f}"/>')


def heart(x, y, s=1.0):
    return (f'<path class="heartf" d="M{x} {y + 10 * s:.1f} C{x - 16 * s:.1f} {y - 2 * s:.1f} {x - 9 * s:.1f} {y - 14 * s:.1f} {x} {y - 6 * s:.1f} '
            f'C{x + 9 * s:.1f} {y - 14 * s:.1f} {x + 16 * s:.1f} {y - 2 * s:.1f} {x} {y + 10 * s:.1f} Z"/>')


def zzz(x, y):
    return J(x, y, 'z', 'c1') + J(x + 12, y - 14, 'z', 'c1') + J(x + 26, y - 30, 'Z', 'c1')


def seated(x, y):
    """A stick person sitting on something at height y + 60; (x, y) is the head."""
    return (f'<circle class="st" cx="{x}" cy="{y}" r="11"/>'
            f'<path class="st" d="M{x} {y + 11} V{y + 58} M{x} {y + 24} L{x + 18} {y + 40} M{x} {y + 24} L{x - 14} {y + 42} '
            f'M{x} {y + 58} H{x + 30} V{y + 92}"/>')


# ------------------------------------------------------------------ the sixteen scenes
def s0000():
    b = ['<rect class="card" x="210" y="20" width="260" height="170" rx="6"/>',
         '<path class="stm" d="M340 20 V190 M210 105 H470"/>',
         '<circle class="bolt" cx="420" cy="60" r="20"/>',
         '<rect class="card" x="180" y="190" width="320" height="16" rx="3"/>',
         '<rect class="sky" x="200" y="150" width="280" height="40"/>']
    # the cat, loaf position
    b.append('<path class="catf" d="M270 190 C268 160 300 150 340 152 C380 154 400 168 402 190 Z"/>')
    b.append('<circle class="catf" cx="292" cy="160" r="20"/>')
    b.append('<path class="catf" d="M276 150 L278 128 L292 142 Z M296 142 L310 128 L310 150 Z"/>')
    b.append('<path class="st" d="M284 160 q4 4 8 0 M296 160 q4 4 8 0"/>')
    b.append('<path class="st" d="M402 186 C440 186 450 160 430 150"/>')
    b.append(zzz(330, 136))
    b.append(say(520, 70, 120, 40, 'purr.', 470, 140, 'c3'))
    b.append(J(100, 120, 'plans for today:', 'c1') + J(100, 142, 'this spot', 'c1'))
    return svg('0 0 680 240', 'A cat asleep on a sunny windowsill, purring', ''.join(b), 't0')


def s0001():
    b = ['<circle class="sky" cx="200" cy="150" r="80"/>',
         ground(234, 90, 310),
         person(200, 120),
         '<path class="st" d="M218 160 h12 v18 h-12 z M230 165 q8 4 0 10"/>',
         clock(90, 60)]
    b.append(think(330, 22, 230, 160, ['coffee', 'a raise', 'a nap', 'the beach house', 'more coffee'], 214, 104))
    b.append(J(200, 90, '5 more minutes', 'c2', 'middle'))
    b.append(J(600, 220, 'the list goes on', 'c1', 'end'))
    return svg('0 0 680 250', 'A sleepy person in a small circle of light holding a mug, with a clock on the wall and a long wish list in a thought bubble', ''.join(b), 't1')


def s0010():
    b = ['<path class="water" d="M40 196 Q80 184 120 196 T200 196 T280 196 T360 196 T440 196 T520 196 T600 196 T640 196"/>',
         '<path class="waterf" d="M40 200 H640 V240 H40 Z"/>',
         '<path class="rockf" d="M260 196 C258 150 300 132 340 132 C390 132 420 156 420 196 Z"/>',
         '<path class="st" d="M312 168 q8 6 16 0 M352 168 q8 6 16 0 M330 184 q10 6 20 0"/>']
    b.append(zzz(420, 130))
    b.append(J(120, 70, 'tide in, tide out,', 'c1', 'middle') + J(120, 92, 'tide in, tide out', 'c1', 'middle'))
    b.append(say(470, 40, 170, 40, 'still here. all good.', 400, 128, 'c3'))
    return svg('0 0 680 250', 'A smiling pebble asleep on the beach while the tide comes in and goes out', ''.join(b), 't2')


def s0011():
    b = [ground(230),
         '<rect class="card" x="500" y="40" width="130" height="190" rx="4"/>',
         '<circle class="fmu" cx="610" cy="140" r="4"/>',
         '<rect class="cardm" x="510" y="56" width="110" height="34" rx="4"/>',
         T(565, 78, 'NOW SERVING: ?', 'small b', 'middle')]
    for i, x in enumerate((420, 340, 260, 180)):
        b.append(person(x, 136, 0.95))
    # cobwebs on the last one in line
    b.append('<path class="stm" d="M160 120 L200 160 M200 120 L160 160 M154 140 H206 M168 128 Q180 140 168 152 M192 128 Q180 140 192 152"/>')
    b.append(think(40, 20, 170, 70, ['my turn soon?'], 170, 118))
    b.append(J(300, 60, 'since Tuesday', 'c2', 'middle'))
    return svg('0 0 680 250', 'A line of people at a closed office door under a sign that says now serving question mark; the last one has cobwebs', ''.join(b), 't3')


def s0100():
    b = [ground(232),
         person(300, 130),
         # the couch held overhead
         '<rect class="card" x="220" y="66" width="170" height="40" rx="8"/>',
         '<rect class="card" x="214" y="56" width="22" height="56" rx="8"/><rect class="card" x="374" y="56" width="22" height="56" rx="8"/>',
         '<path class="st" d="M300 152 L270 108 M300 152 L336 108"/>',
         '<rect class="card" x="530" y="196" width="70" height="34" rx="3"/><rect class="card" x="450" y="160" width="90" height="70" rx="3"/>',
         T(495, 200, 'FRAGILE?', 'small b', 'middle')]
    b.append(say(410, 40, 200, 40, 'where does this go?', 360, 90))
    b.append(J(110, 200, 'paid in pizza', 'c3', 'middle'))
    return svg('0 0 680 250', 'A cheerful friend lifting a couch overhead and asking where it goes, next to a pile of boxes', ''.join(b), 't4')


def car(x, y, w=260):
    h = 52
    return (f'<path class="card" d="M{x} {y + h} V{y + 22} Q{x} {y + 12} {x + 14} {y + 10} L{x + w * .25:.0f} {y + 6} L{x + w * .38:.0f} {y - 30} '
            f'H{x + w * .72:.0f} L{x + w * .86:.0f} {y + 6} Q{x + w} {y + 10} {x + w} {y + 26} V{y + h} Z"/>'
            f'<path class="cardm" d="M{x + w * .41:.0f} {y - 22} H{x + w * .55:.0f} V{y + 4} H{x + w * .33:.0f} Z M{x + w * .58:.0f} {y - 22} H{x + w * .7:.0f} L{x + w * .8:.0f} {y + 4} H{x + w * .58:.0f} Z"/>'
            f'<circle class="card" cx="{x + w * .2:.0f}" cy="{y + h}" r="20"/><circle class="card" cx="{x + w * .8:.0f}" cy="{y + h}" r="20"/>')


def s0101():
    b = [ground(232), car(260, 158, 280),
         person(170, 128),
         '<circle class="iron" cx="196" cy="168" r="6"/><path class="st" d="M188 168 L178 166"/>']
    b.append(think(20, 20, 220, 70, ['everything.', 'tonight.'], 162, 110))
    b.append(say(420, 40, 220, 40, 'what does this button do?', 380, 120))
    return svg('0 0 680 250', 'A teenager twirling car keys next to a car, thinking about everything tonight', ''.join(b), 't5')


def s0110():
    b = ['<path class="land" d="M40 60 H230 L260 110 L250 170 L280 220 H40 Z"/>',
         '<path class="land" d="M640 60 H450 L420 120 L440 170 L400 220 H640 Z"/>',
         '<path class="waterf" d="M280 220 C300 200 380 200 400 220 Z"/>',
         '<path class="water" d="M296 214 C320 204 360 204 384 214"/>',
         '<path class="stm dash" d="M250 110 L262 140 M430 120 L420 150 M256 170 L270 196 M440 170 L424 196"/>']
    b.append('<rect class="cardm" x="300" y="70" width="80" height="54" rx="3" transform="rotate(-8 340 97)"/>')
    b.append(T(340, 104, 'map', 'small b', 'middle'))
    b.append(J(340, 50, 'never opened', 'c2', 'middle'))
    b.append(say(470, 8, 170, 40, 'just passing through', 400, 200, 'c1'))
    return svg('0 0 680 240', 'A small river at the bottom of a deep canyon it carved, with an unopened map floating above', ''.join(b), 't6')


def s0111():
    b = ['<path class="cloud" d="M170 190 C150 190 140 170 160 160 C156 138 190 130 200 146 C210 126 250 126 258 148 C280 136 304 152 292 170 C312 176 304 196 284 196 H180 Z"/>',
         person(230, 82, 1.0, 'st', legs=False),
         '<path class="st" d="M222 92 Q230 120 238 92"/>',  # beard
         '<path class="bolt" d="M262 100 L282 70 L276 92 L296 88 L270 128 L276 104 Z"/>',
         '<path class="iron" d="M216 66 L220 54 L226 62 L230 50 L234 62 L240 54 L244 66 Z"/>']
    b.append(think(330, 20, 170, 60, ['I want THAT.'], 252, 70))
    b.append('<rect class="card" x="520" y="140" width="110" height="80" rx="4"/><path class="st" d="M510 142 L575 104 L640 142"/>')
    b.append(J(575, 190, 'home', 'c1', 'middle'))
    b.append(J(575, 238, '"we need to talk"', 'c2', 'middle'))
    return svg('0 0 680 250', 'A crowned figure with a beard on a cloud holding a lightning bolt and wanting something, while at home someone says we need to talk', ''.join(b), 't7')


def s1000():
    b = [ground(232),
         # rocking chair
         '<path class="st" d="M180 232 Q240 248 300 232 M200 160 V226 M280 196 V226 M200 196 H280 M190 100 L200 160"/>',
         seated(220, 120),
         '<rect class="card" x="380" y="170" width="100" height="10" rx="2"/><path class="st" d="M394 180 V232 M466 180 V232"/>',
         '<rect class="card" x="404" y="132" width="34" height="38" rx="5"/><rect class="iron" x="400" y="124" width="42" height="10" rx="2"/>',
         '<rect class="card" x="452" y="150" width="22" height="20" rx="3"/>',
         heart(312, 92, 0.9)]
    b.append(say(480, 40, 170, 50, 'sit. eat something.', 250, 104, 'c3'))
    b.append(J(420, 116, 'still sealed', 'c2', 'middle'))
    return svg('0 0 680 250', 'A grandma in a rocking chair next to a jar she cannot open, telling you to sit and eat something', ''.join(b), 't8')


def s1001():
    b = [ground(232), car(150, 150, 380),
         '<circle class="st" cx="390" cy="138" r="10"/><path class="st" d="M390 148 V170 M390 156 L410 162"/>',
         '<circle class="st" cx="300" cy="138" r="10"/><path class="st" d="M300 148 V170 M300 156 L350 128"/>',
         '<circle class="card" cx="420" cy="160" r="8"/>',
         clock(470, 100, 12)]
    b.append(say(40, 20, 230, 50, 'left! no, the OTHER left!', 296, 128))
    b.append(J(560, 60, 'shops close at six', 'c1', 'middle'))
    return svg('0 0 680 250', 'A car with a driver in front and a passenger in the back pointing and shouting directions', ''.join(b), 't9')


def s1010():
    b = ['<rect class="card" x="120" y="30" width="440" height="200" rx="4"/>']
    for r in range(4):
        y = 40 + r * 48
        b.append(f'<path class="st" d="M120 {y + 44} H560"/>')
        for i in range(19):
            x = 132 + i * 22 + (r * 7) % 9
            h = 30 + (i * 7 + r * 5) % 12
            b.append(f'<rect class="{"cardm" if (i + r) % 3 else "fsoft fhi"}" x="{x}" y="{y + 44 - h}" width="16" height="{h}" rx="2"/>')
    b.append('<rect class="card" x="250" y="96" width="180" height="40" rx="6"/>')
    b.append(T(340, 121, 'QUIET, PLEASE', 'ts', 'middle'))
    b.append(J(600, 120, 'ask me', 'c3', 'middle') + J(600, 142, 'anything', 'c3', 'middle') + J(600, 164, '(quietly)', 'c1', 'middle'))
    return svg('0 0 680 250', 'Tall shelves of books in a library under a sign that says quiet, please', ''.join(b), 't10')


def s1011():
    b = [ground(232),
         '<rect class="rockf" x="230" y="186" width="120" height="46" rx="3"/>',
         '<circle class="rockf" cx="290" cy="76" r="18"/>',
         '<path class="rockf" d="M270 96 H310 L318 186 H262 Z"/>',
         '<path class="rockf" d="M308 104 L340 70 L350 78 L316 116 Z"/>',
         # the pigeon on the head
         '<path class="card" d="M276 58 C276 44 296 40 304 50 L314 48 L306 56 C304 62 292 64 276 58 Z"/>',
         '<circle class="inkf" cx="300" cy="50" r="1.8"/>']
    b.append(think(380, 20, 200, 60, ['please. leave.'], 300, 70))
    b.append(J(560, 200, 'every single day', 'c2', 'middle'))
    b.append(J(110, 120, 'knows who', 'c1', 'middle') + J(110, 142, 'parked badly', 'c1', 'middle'))
    return svg('0 0 680 250', 'A stone statue in the park with a pigeon on its head, thinking please leave', ''.join(b), 't11')


def s1100():
    b = [ground(232),
         '<rect class="card" x="300" y="110" width="200" height="122" rx="4"/>',
         '<rect class="cardm" x="290" y="98" width="220" height="14" rx="3"/>',
         '<path class="st" d="M330 112 V150 Q330 168 350 168 H380"/>',
         # plumber lying on the floor, head under the sink
         '<circle class="st" cx="360" cy="206" r="11"/><path class="st" d="M349 206 H220 M300 206 L280 186 M260 206 L230 232 M240 206 L200 232"/>',
         '<path class="iron" d="M380 186 L404 176 L410 184 L386 196 Z"/>',
         '<rect class="card" x="90" y="200" width="70" height="32" rx="4"/><path class="st" d="M110 200 V192 H140 V200"/>']
    b.append(say(470, 30, 170, 40, 'fixed. bye!', 400, 150, 'c3'))
    b.append(J(200, 70, 'next call: after lunch', 'c1', 'middle'))
    return svg('0 0 680 250', 'A plumber lying under a sink with a wrench, saying fixed, bye', ''.join(b), 't12')


def s1101():
    b = ['<rect class="card" x="210" y="150" width="200" height="10" rx="2"/>',
         '<path class="st" d="M230 160 V232 M390 160 V232"/>', ground(232),
         '<path class="card" d="M290 150 L300 104 H372 L366 150 Z"/>',
         '<circle class="st" cx="250" cy="96" r="11"/><path class="st" d="M250 107 V150"/>',
         # many arms, typing very fast
         '<path class="st" d="M250 118 L296 140 M250 122 L290 132 M250 126 L300 146 M250 130 L284 150"/>',
         '<rect class="card" x="460" y="60" width="90" height="70" rx="4"/><rect class="warn" x="460" y="60" width="90" height="18" rx="4"/>',
         T(505, 112, 'FRIDAY', 'ts', 'middle')]
    b.append(think(20, 20, 180, 60, ['the moon.', 'and a bit more.'], 242, 82))
    b.append(J(600, 180, 'just one more', 'c2', 'middle') + J(600, 200, 'feature', 'c2', 'middle'))
    return svg('0 0 680 250', 'A founder typing with many arms at once, a calendar saying Friday, thinking about the moon', ''.join(b), 't13')


def s1110():
    b = ['<circle class="glow" cx="340" cy="125" r="112"/>',
         '<circle class="ringhi solid" cx="340" cy="125" r="104"/>']
    pts = [(290, 70), (380, 62), (410, 120), (300, 160), (360, 180), (260, 118), (430, 168), (330, 110), (390, 96), (250, 160)]
    for i, (x, y) in enumerate(pts):
        b.append(f'<circle class="{"fhi" if i % 2 else "fmu"}" cx="{x}" cy="{y}" r="{3 + i % 3}"/>')
    b.append(person(340, 112, 0.35))
    b.append('<circle class="bolt" cx="268" cy="92" r="9"/>')
    b.append(J(120, 90, 'nothing missing', 'c3', 'middle'))
    b.append(J(560, 90, 'nothing to do', 'c3', 'middle'))
    b.append(J(560, 190, 'slightly short', 'c1', 'middle') + J(560, 210, 'on plot', 'c1', 'middle'))
    return svg('0 0 680 250', 'One glowing circle with everything inside it, stars, planets, a tiny person, and nothing missing', ''.join(b), 't14')


def s1111():
    b = [ground(232),
         person(300, 110, 1.1),
         '<path class="iron" d="M286 92 L290 78 L296 88 L300 74 L304 88 L310 78 L314 92 Z"/>',
         # the big glove, raised
         '<path class="st" d="M300 136 L342 104"/>',
         '<rect class="iron" x="336" y="70" width="40" height="44" rx="10"/>']
    for i, c in enumerate(('fhi', 'fdo', 'fbe', 'sunf', 'fmu')):
        b.append(f'<circle class="{c}" cx="{344 + i * 6}" cy="{82 + (i % 2) * 8}" r="3.2"/>')
    b.append(J(392, 70, '*snap*', 'c2'))
    b.append(think(430, 100, 180, 70, ['more.'], 316, 100))
    b.append(J(130, 80, 'has: everything', 'c1', 'middle'))
    b.append(J(130, 104, 'wants: more', 'c2', 'middle'))
    return svg('0 0 680 250', 'A crowned figure raising a big glove with gems and snapping, still thinking more', ''.join(b), 't15')


SCENES = {f'{i:04b}': f for i, f in enumerate([s0000, s0001, s0010, s0011, s0100, s0101, s0110, s0111,
                                                s1000, s1001, s1010, s1011, s1100, s1101, s1110, s1111])}


# ------------------------------------------------------------------ the sliders
LOW, HIGH = 0.22, 0.85


def sliders(state=START):
    top, bot = 50, 210
    b = []
    for i, (lab, lo, hi) in enumerate(SETTINGS):
        x = 120 + i * 146
        on = state[i] == '1'
        dy = -(HIGH - LOW) * (bot - top) if on else 0
        ky = bot - LOW * (bot - top)
        cls = 'fdo' if i == 3 else 'fhi'
        b.append(f'<g class="sw" data-i="{i}" role="switch" tabindex="0" aria-checked="{"true" if on else "false"}" aria-label="{lab}: low or high">')
        b.append(f'<rect class="hit" x="{x - 70}" y="{top - 20}" width="140" height="{bot - top + 80}"/>')
        b.append(f'<rect class="slot" x="{x - 7}" y="{top}" width="14" height="{bot - top}" rx="7"/>')
        b.append(f'<path class="stm dash" d="M{x - 22} {top} H{x + 22}"/>')
        # the colored level grows from the bottom; scaled around the bottom so it can animate
        b.append(f'<rect class="{cls} fsoft lvl" x="{x - 7}" y="{top}" width="14" height="{bot - top}" rx="7" '
                 f'style="transform-origin:{x}px {bot}px;transform:scaleY({HIGH if on else LOW})"/>')
        b.append(f'<rect class="knobf" x="{x - 22}" y="{ky - 9:.0f}" width="44" height="18" rx="5" style="transform:translateY({dy:.0f}px)"/>')
        b.append(T(x, bot + 28, lab, 'small b', 'middle'))
        b.append(f'<text class="small val" x="{x}" y="{bot + 45}" text-anchor="middle" data-lo="{lo}" data-hi="{hi}">{hi if on else lo}</text>')
        b.append('</g>')
    b.append(T(70, top + 4, 'all of it', 'small faint', 'end'))
    return ('<svg class="chart ill sliders" viewBox="0 0 680 270" role="group" aria-label="Four settings for one point of view. Tap a slider to switch it between low and high.">'
            + ''.join(b) + '</svg>')


JS = r"""
(function(){
  var toys=document.querySelectorAll('.toy');
  toys.forEach(function(toy){
    var st=toy.getAttribute('data-start').split(''), lo=%LOW%, hi=%HIGH%, span=%SPAN%;
    function draw(){
      var key=st.join('');
      toy.querySelectorAll('.sw').forEach(function(g){
        var i=+g.getAttribute('data-i'), on=st[i]==='1';
        g.setAttribute('aria-checked',on?'true':'false');
        g.querySelector('.lvl').style.transform='scaleY('+(on?hi:lo)+')';
        g.querySelector('.knobf').style.transform='translateY('+(on?-span:0)+'px)';
        var v=g.querySelector('.val'); v.textContent=v.getAttribute(on?'data-hi':'data-lo');
      });
      toy.querySelectorAll('.scene').forEach(function(s){s.classList.toggle('on',s.getAttribute('data-k')===key);});
    }
    function flip(g){var i=+g.getAttribute('data-i'); st[i]=st[i]==='1'?'0':'1'; draw();}
    toy.querySelectorAll('.sw').forEach(function(g){
      g.addEventListener('click',function(){flip(g);});
      g.addEventListener('keydown',function(e){if(e.key===' '||e.key==='Enter'){e.preventDefault();flip(g);}});
    });
    var r=toy.querySelector('.reset'); if(r) r.addEventListener('click',function(){st=toy.getAttribute('data-start').split('');draw();});
    var x=toy.querySelector('.rand'); if(x) x.addEventListener('click',function(){
      var k=st.join(''), n; do{n=('000'+Math.floor(Math.random()*16).toString(2)).slice(-4);}while(n===k); st=n.split(''); draw();});
    toy.querySelector('.bar').hidden=false; toy.querySelector('.hint').hidden=false;
  });
})();
"""


def widget(caption='Four settings for one point of view, and what each mix of them looks like.'):
    top, bot = 50, 210
    js = (JS.replace('%LOW%', str(LOW)).replace('%HIGH%', str(HIGH))
          .replace('%SPAN%', f'{(HIGH - LOW) * (bot - top):.0f}'))
    scenes = []
    for k, fn in SCENES.items():
        title, text = TEXTS[k]
        on = ' on' if k == START else ''
        scenes.append(f'<div class="scene{on}" data-k="{k}">{fn()}<div class="say"><h5>{title}</h5><p>{text}</p></div></div>')
    return (f'<figure class="fig toy" data-start="{START}">'
            f'<p class="lead">{caption}</p>'
            f'<p class="hint" hidden>Tap a slider to turn it up or down.</p>'
            f'{sliders()}'
            f'<div class="bar" hidden><button type="button" class="reset">back to factory settings</button>'
            f'<button type="button" class="rand">surprise me</button></div>'
            f'{"".join(scenes)}'
            f'<script>{js}</script></figure>')
