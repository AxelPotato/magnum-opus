"""Illustrations for Part two (added to figs4's) and Part three (inline SVG, theme-aware). Imported by build_html.py.

Same drawing helpers and hand as figs2.py and figs4.py. CSS_EXTRA holds the few rules these figures add.
"""
import math

from figs2 import T, arrow, person, svg

CSS_EXTRA = r"""
.chart .flame{fill:#F2C14E;stroke:var(--ink);stroke-width:1.6;stroke-linejoin:round}
.chart .glow{fill:#F2C14E;fill-opacity:.22;stroke:none}
.chart .warn{fill:var(--driven);stroke:var(--ink);stroke-width:1.6}
.chart .tape{fill:#E9D9A6;stroke:var(--ink);stroke-width:1.4;fill-opacity:.95}
.chart .water{fill:none;stroke:var(--drifting);stroke-width:2.6;stroke-linecap:round}
.chart .waterf{fill:var(--drifting);fill-opacity:.16;stroke:none}
.chart .tankf{fill:var(--muted);fill-opacity:.28;stroke:none}
.chart .slot{fill:var(--paper);stroke:var(--rule);stroke-width:1.5}
.chart .knobf{fill:var(--card);stroke:var(--ink);stroke-width:2.2}
.chart .geneon{fill:var(--high);stroke:none}
.chart .geneoff{fill:var(--muted);fill-opacity:.25;stroke:none}
.chart .land{fill:var(--muted);fill-opacity:.12;stroke:var(--ink);stroke-width:2;stroke-linejoin:round}
.chart .ringhi{fill:none;stroke:var(--high);stroke-width:2;stroke-dasharray:4 5}
.chart .ringhi.solid{stroke-dasharray:none}
.chart .fhis{fill:var(--high);fill-opacity:.14;stroke:none}
.chart .fdos{fill:var(--driven);fill-opacity:.14;stroke:none}
.chart .fbes{fill:var(--drifting);fill-opacity:.14;stroke:none}
.chart .sbe2{fill:none;stroke:var(--drifting);stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.chart .sdo2{fill:none;stroke:var(--driven);stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.chart .iron{fill:var(--driven);stroke:var(--ink);stroke-width:1.6}
.chart .inkf{fill:var(--ink)}
.chart text.faint{fill:var(--muted);opacity:.8}
"""


def _lamp(x, y, lit=True):
    """A small oil lamp; (x, y) is the base of the wick."""
    b = [f'<path class="card" d="M{x - 46} {y} Q{x - 40} {y + 30} {x} {y + 30} Q{x + 40} {y + 30} {x + 52} {y + 4} L{x + 70} {y - 4} L{x + 52} {y - 6} Q{x + 10} {y - 8} {x - 46} {y} Z"/>',
         f'<path class="st" d="M{x - 30} {y + 30} V{y + 40} H{x + 30} V{y + 30}"/>']
    if lit:
        b.append(f'<ellipse class="glow" cx="{x + 60}" cy="{y - 30}" rx="34" ry="40"/>')
        b.append(f'<path class="flame" d="M{x + 60} {y - 6} C{x + 46} {y - 20} {x + 54} {y - 38} {x + 62} {y - 52} C{x + 64} {y - 36} {x + 76} {y - 22} {x + 60} {y - 6} Z"/>')
    return ''.join(b)


# ================================================================== PART TWO

# ------------------------------------------------------------------ four settings (step 2)
def fig_settings():
    u = 'se'
    b = []
    cols = [('what it can know', 'a little', 0.22), ('what it can do', 'a little', 0.25), ('how long it lasts', 'a little', 0.18), ('what it wants', 'quite a lot', 0.85)]
    top, bot = 60, 250
    for i, (lab, val, lvl) in enumerate(cols):
        x = 120 + i * 146
        b.append(f'<rect class="slot" x="{x - 7}" y="{top}" width="14" height="{bot - top}" rx="7"/>')
        b.append(f'<path class="stm dash" d="M{x - 22} {top} H{x + 22}"/>')
        ky = bot - lvl * (bot - top)
        cls = 'fdo' if i == 3 else 'fhi'
        b.append(f'<rect class="{cls} fsoft" x="{x - 7}" y="{ky:.0f}" width="14" height="{bot - ky:.0f}" rx="7"/>')
        b.append(f'<rect class="knobf" x="{x - 22}" y="{ky - 9:.0f}" width="44" height="18" rx="5"/>')
        b.append(T(x, bot + 28, lab, 'small b', 'middle'))
        b.append(T(x, bot + 45, val, 'small', 'middle'))
    b.append(T(70, top + 4, 'all of it', 'small faint', 'end'))
    b.append(T(340, 30, 'One point of view, set up', 't', 'middle'))
    return svg('0 0 680 320', 'Four sliders for one point of view: what it can know, what it can do and how long it lasts are set low, and what it wants is set high', ''.join(b), u)


# ------------------------------------------------------------------ the cell keeps the whole plan (step 2)
def fig_cell():
    u = 'ce'
    b = []
    b.append('<ellipse class="card" cx="250" cy="170" rx="190" ry="130"/>')
    b.append('<ellipse class="cardm" cx="250" cy="170" rx="118" ry="78"/>')
    on = {7, 8, 9, 22}
    k = 0
    for r in range(4):
        for c in range(9):
            x, y = 170 + c * 18, 128 + r * 24
            b.append(f'<rect class="{"geneon" if k in on else "geneoff"}" x="{x}" y="{y}" width="12" height="14" rx="2"/>')
            k += 1
    b.append(T(250, 116, 'the whole plan for you', 'small b', 'middle'))
    b.append('<path class="leader" d="M318 140 C380 120 440 100 470 96"/>')
    b.append(T(478, 92, 'the liver part, on', 'small b'))
    b.append('<path class="leader" d="M300 210 C380 240 440 250 470 254"/>')
    b.append(T(478, 250, 'the eye, the nerve and', 'small'))
    b.append(T(478, 266, 'the rest: switched off,', 'small'))
    b.append(T(478, 282, 'still there', 'small'))
    b.append(T(250, 332, 'one liver cell', 't', 'middle'))
    return svg('0 0 680 350', 'A liver cell whose nucleus holds the complete plan for the body, with only the liver part switched on and the rest switched off but kept', ''.join(b), u)


# ------------------------------------------------------------------ the warning light (step 3)
def _dash(x, taped):
    b = [f'<rect class="card" x="{x}" y="40" width="250" height="150" rx="40"/>']
    for cx, lab in ((x + 72, 'speed'), (x + 178, 'fuel')):
        b.append(f'<circle class="cardm" cx="{cx}" cy="105" r="40"/>')
        b.append(f'<path class="st" d="M{cx} 105 L{cx - 18} 82"/>')
        b.append(T(cx, 132, lab, 'small', 'middle'))
    lx, ly = x + 125, 166
    if taped:
        b.append(f'<circle class="warn" cx="{lx}" cy="{ly}" r="10"/>')
        b.append(f'<rect class="tape" x="{lx - 22}" y="{ly - 11}" width="44" height="22" rx="2" transform="rotate(-8 {lx} {ly})"/>')
    else:
        b.append(f'<circle class="glow" cx="{lx}" cy="{ly}" r="22"/>')
        b.append(f'<circle class="warn" cx="{lx}" cy="{ly}" r="10"/>')
    return ''.join(b)


def fig_warning():
    u = 'wn'
    b = [_dash(60, False), _dash(370, True)]
    b.append(T(185, 222, 'the message', 't', 'middle'))
    b.append(T(185, 240, 'the reason anyone opens the hood', 'small', 'middle'))
    b.append(T(495, 222, 'the other option', 't', 'middle'))
    b.append(T(495, 240, 'most of us have tried it', 'small', 'middle'))
    return svg('0 0 680 260', 'Two car dashboards: on one the warning light is on, on the other a piece of tape covers it', ''.join(b), u)


# ------------------------------------------------------------------ need and love (step 3)
def fig_needlove():
    u = 'nl'
    b = []
    b.append(T(170, 30, 'Need', 't', 'middle'))
    b.append(T(170, 48, 'I need you so that I feel whole', 'small', 'middle'))
    b.append(person(130, 100, 0.9, 'st'))
    b.append(person(220, 100, 0.9, 'st'))
    b.append('<path class="stm dash" d="M92 70 h76 v130 h-76 Z"/>')
    b.append('<path class="stm dash" d="M182 70 h76 v130 h-76 Z"/>')
    b.append(f'<path class="sdo2" d="M150 136 C165 126 180 126 196 134" marker-end="url(#a{u}do)"/>')
    b.append('<path class="stm dash" d="M340 24 V250"/>')
    b.append(T(510, 30, 'Love', 't', 'middle'))
    b.append(T(510, 48, 'you are part of what I am', 'small', 'middle'))
    b.append('<ellipse class="fhis" cx="510" cy="140" rx="120" ry="78"/>')
    b.append('<ellipse class="ringhi" cx="510" cy="140" rx="120" ry="78"/>')
    b.append(person(470, 100, 0.9, 'st'))
    b.append(person(550, 100, 0.9, 'st'))
    b.append(T(510, 244, 'one outline around both', 'small', 'middle'))
    b.append(T(170, 244, 'two outlines, one reaching', 'small', 'middle'))
    return svg('0 0 680 262', 'Need: two people each in their own outline, one reaching for the other. Love: two people inside one shared outline', ''.join(b), u)


# ------------------------------------------------------------------ the turn (step 4)
def fig_turn():
    u = 'tu'
    b = []
    b.append('<path class="stm dash" d="M40 60 H640"/>')
    b.append(T(640, 50, 'one whole', 'small b', 'end'))
    b.append('<path class="life" d="M60 70 C150 90 240 270 340 270 C440 270 530 90 620 66"/>')
    b.append(f'<path class="stm2" d="M140 120 L190 176" marker-end="url(#a{u}mu)"/>')
    b.append(f'<path class="hi" d="M490 176 L540 120" marker-end="url(#a{u}hi)"/>')
    b.append('<circle class="fhi" cx="340" cy="270" r="8"/>')
    b.append(T(340, 300, 'the bottom point: the signal flips', 'small b', 'middle'))
    b.append(T(120, 210, 'more separate feels good', 'small b', 'middle'))
    b.append(T(120, 226, 'my room, my money,', 'small', 'middle'))
    b.append(T(120, 242, 'my name on the door', 'small', 'middle'))
    b.append(T(560, 210, 'a step toward unity', 'small b', 'middle'))
    b.append(T(560, 226, 'feels good, and it lasts', 'small', 'middle'))
    b.append(T(200, 40, 'first half', 'ts', 'middle'))
    b.append(T(480, 40, 'second half', 'ts', 'middle'))
    return svg('0 0 680 320', 'A curve that goes down toward separation in the first half, reaches a bottom point where the signal flips, and climbs back toward one in the second half', ''.join(b), u)


# ------------------------------------------------------------------ a lamp lit from a lamp (step 5)
def fig_lamps():
    u = 'lp'
    b = [_lamp(160, 150), _lamp(440, 150)]
    b.append(f'<path class="hi dash" d="M250 96 C300 60 400 60 470 92" marker-end="url(#a{u}hi)"/>')
    b.append(T(360, 52, 'the flame is passed', 'small b', 'middle'))
    b.append(T(340, 230, 'Nothing passes across, and the second one still burns.', 't', 'middle'))
    return svg('0 0 680 250', 'Two oil lamps: the second is lit from the first, and both burn', ''.join(b), u)


# ------------------------------------------------------------------ the same two hours (step 7)
def _meter(x, y, lvl, cls):
    h = 120
    b = [f'<rect class="card" x="{x}" y="{y}" width="56" height="{h}" rx="8"/>',
         f'<rect class="st" x="{x + 18}" y="{y - 10}" width="20" height="10" rx="2"/>',
         f'<rect class="{cls} fsoft" x="{x + 6}" y="{y + h - 6 - lvl * (h - 12):.0f}" width="44" height="{lvl * (h - 12):.0f}" rx="4"/>']
    return ''.join(b)


def fig_hours():
    u = 'hr'
    b = []
    b.append(T(170, 30, 'two hours on guard', 't', 'middle'))
    b.append(T(510, 30, 'two hours with an old friend', 't', 'middle'))
    for cx, lvl0, lvl1, cls in ((170, 0.8, 0.25, 'fmu'), (510, 0.8, 0.95, 'fhi')):
        b.append(_meter(cx - 90, 70, lvl0, 'fmu'))
        b.append(f'<path class="stm2" d="M{cx - 20} 130 H{cx + 20}" marker-end="url(#a{u}mu)"/>')
        b.append(_meter(cx + 34, 70, lvl1, cls))
        b.append(T(cx - 62, 214, 'before', 'small', 'middle'))
        b.append(T(cx + 62, 214, 'after', 'small', 'middle'))
    b.append(T(340, 250, 'Just as much talking. The guarding is what costs.', 'small b', 'middle'))
    return svg('0 0 680 266', 'Two pairs of battery meters: after two hours on guard the meter is low, after two hours with an old friend it is higher than before', ''.join(b), u)



# ------------------------------------------------------------------ the cloth lifted by one jewel (step 8)
def fig_cloth():
    u = 'cl'
    base = 200

    def y(x):
        k = (x - 340) / 120
        return base - 150 * math.exp(-k * k)
    path = 'M' + ' L'.join(f'{x} {y(x):.1f}' for x in range(20, 661, 8))
    b = [f'<path class="st faint" d="M10 {base + 4} H670"/>',
         f'<path class="fhi fsoft" style="fill-opacity:.18" d="{path} L660 {base} L20 {base} Z"/>',
         f'<path class="hi" d="{path}"/>',
         f'<path class="stm2 dash" d="M340 14 V{y(340) - 12:.0f}"/>']
    for x in range(20, 661, 40):
        r = 8 if x == 340 else 5
        b.append(f'<circle class="fhi" cx="{x}" cy="{y(x):.1f}" r="{r}"/>')
    b.append('<circle class="st" cx="340" cy="%.1f" r="8"/>' % y(340))
    b.append(T(372, 40, 'lifted by one jewel', 'small'))
    b.append(T(560, base - 14, 'the far edge rises last', 'small', 'middle'))
    return svg('0 0 680 220', 'A cloth with jewels, lifted by one jewel: that jewel is highest, the nearest jewels rise with it, and the far edges leave the table last', ''.join(b), u)

# ------------------------------------------------------------------ the tank and the mill (step 7)
def fig_mill():
    u = 'ml'
    b = []
    # the tank
    b.append('<rect class="card" x="60" y="70" width="140" height="170" rx="12"/>')
    b.append('<rect class="tankf" x="64" y="160" width="132" height="76" rx="8"/>')
    for k, ln in enumerate(('I have this much,', 'I spend it,', 'I guard the rest')):
        b.append(T(130, 270 + k * 16, ln, 'small', 'middle'))
    b.append(T(130, 50, 'a tank', 't', 'middle'))
    # the river and the mill
    b.append('<path class="waterf" d="M290 210 C380 196 470 222 560 208 C600 202 630 206 660 210 V250 H290 Z"/>')
    for yy in (220, 236):
        b.append(f'<path class="water" d="M300 {yy} C380 {yy - 10} 470 {yy + 12} 560 {yy - 2} C600 {yy - 8} 630 {yy - 2} 650 {yy}"/>')
    b.append(f'<path class="water" d="M590 186 H646" marker-end="url(#a{u}ink)"/>')
    b.append('<path class="card" d="M330 230 V120 L380 90 L430 120 V230 Z"/>')
    cx, cy, r = 500, 184, 50
    b.append(f'<circle class="st" cx="{cx}" cy="{cy}" r="{r}"/>')
    b.append(f'<circle class="st" cx="{cx}" cy="{cy}" r="6"/>')
    for k in range(8):
        a = math.radians(k * 45)
        b.append(f'<path class="st" d="M{cx + 6 * math.cos(a):.1f} {cy + 6 * math.sin(a):.1f} L{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}"/>')
        b.append(f'<path class="st" d="M{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f} l{10 * math.cos(a + 1.2):.1f} {10 * math.sin(a + 1.2):.1f}"/>')
    b.append(f'<path class="hi" d="M560 120 A70 70 0 0 1 570 170" marker-end="url(#a{u}hi)"/>')
    b.append(T(470, 50, 'a mill on a river', 't', 'middle'))
    for k, ln in enumerate(('the water turns the wheel', 'and flows on to the next mill')):
        b.append(T(470, 270 + k * 16, ln, 'small', 'middle'))
    return svg('0 0 680 310', 'A closed tank with a level that only goes down, next to a water mill whose wheel is turned by a river that flows on', ''.join(b), u)


# ------------------------------------------------------------------ paths drawn for different people (why the paths differ)
def fig_paths():
    u = 'pa'
    b = []
    b.append('<path class="land" d="M40 290 L250 120 L340 60 L430 120 L640 290 Z"/>')
    b.append('<circle class="fhi" cx="340" cy="62" r="8"/>')
    b.append(T(340, 40, 'the same place', 'small b', 'middle'))
    b.append('<path class="sdo2 dash" d="M90 290 C150 250 200 230 230 200 C260 170 300 120 336 70"/>')
    b.append('<path class="sbe2 dash" d="M340 290 C300 250 380 220 330 180 C290 150 380 120 340 72"/>')
    b.append('<path class="shi dash" d="M590 290 C520 250 470 230 450 190 C430 150 380 110 344 70"/>')
    b.append(T(90, 312, 'herders crossing a desert', 'small', 'middle'))
    b.append(T(340, 312, 'monks on a mountain', 'small', 'middle'))
    b.append(T(590, 312, 'merchants on a trade road', 'small', 'middle'))
    return svg('0 0 680 326', 'One mountain with three paths drawn for different people, starting far apart and meeting at the same summit', ''.join(b), u)


# ------------------------------------------------------------------ where does the border of you sit? (the end of Part two)
def fig_border():
    u = 'bo'
    b = []
    cx, cy = 340, 184
    rings = ((56, 96), (130, 116), (214, 136), (318, 152))
    for rx, ry in rings:
        b.append(f'<ellipse class="ringm" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>')
    b.append(T(cx + 56 + 8, cy + 4, 'the skin?', 'small b'))
    b.append(T(cx - 130 - 8, cy + 4, 'the room?', 'small b', 'end'))
    b.append(T(cx + 214 + 8, cy + 4, 'your people?', 'small b'))
    b.append(T(cx, cy - 152 - 8, 'further?', 'small b', 'middle'))
    b.append(person(cx, cy - 46, 1.0, 'st'))
    return svg('0 0 680 346', 'A person in the middle of several dashed outlines, each a possible border: the skin, the room, your people, further', ''.join(b), u)


# ================================================================== PART THREE

# ------------------------------------------------------------------ eight conditions (the opening)
def _ic(kind, x, y):
    """A 48px icon centred on (x, y)."""
    if kind == 'wish':
        return f'<path class="flame" d="M{x} {y + 20} C{x - 20} {y + 6} {x - 12} {y - 10} {x} {y - 24} C{x + 4} {y - 8} {x + 20} {y + 2} {x} {y + 20} Z"/>'
    if kind == 'goal':
        return (f'<path class="st" d="M{x - 12} {y + 22} V{y - 22}"/>'
                f'<path class="cardhi" d="M{x - 12} {y - 22} H{x + 18} L{x + 10} {y - 12} L{x + 18} {y - 2} H{x - 12} Z"/>')
    if kind == 'discipline':
        o = [f'<rect class="card" x="{x - 22}" y="{y - 18}" width="44" height="40" rx="5"/>', f'<path class="st" d="M{x - 22} {y - 6} H{x + 22} M{x - 12} {y - 24} V{y - 14} M{x + 12} {y - 24} V{y - 14}"/>']
        for i in range(3):
            o.append(f'<path class="shi" d="M{x - 15 + i * 12} {y + 8} l3 4 l6 -8"/>')
        return ''.join(o)
    if kind == 'attention':
        return (f'<path class="cone" d="M{x - 4} {y - 6} L{x + 26} {y - 22} L{x + 26} {y + 10} Z"/>'
                f'<rect class="card" x="{x - 26}" y="{y - 12}" width="24" height="14" rx="3" transform="rotate(-8 {x} {y})"/>')
    if kind == 'giving':
        return (f'<path class="st" d="M{x - 24} {y + 10} C{x - 10} {y + 22} {x + 10} {y + 22} {x + 24} {y + 10}"/>'
                f'<path class="heartf" d="M{x} {y + 2} C{x - 14} {y - 8} {x - 10} {y - 22} {x} {y - 14} C{x + 10} {y - 22} {x + 14} {y - 8} {x} {y + 2} Z"/>')
    if kind == 'mirror':
        return (f'<ellipse class="card" cx="{x}" cy="{y - 4}" rx="16" ry="21"/>'
                f'<path class="stm" d="M{x - 6} {y - 14} L{x + 4} {y - 22} M{x - 8} {y - 4} L{x + 8} {y - 16}"/>'
                f'<path class="st" d="M{x} {y + 17} V{y + 24} M{x - 10} {y + 24} H{x + 10}"/>')
    if kind == 'friends':
        return person(x - 12, y - 18, 0.44, 'st') + person(x + 12, y - 18, 0.44, 'st')
    if kind == 'further':
        return (f'<path class="stm dash" d="M{x - 26} {y + 22} L{x + 26} {y - 4}"/>'
                + person(x - 14, y - 10, 0.36, 'st') + person(x + 14, y - 24, 0.36, 'st'))
    return ''


CONDITIONS = [('wish', 'your wish'), ('goal', 'a goal'), ('discipline', 'discipline'), ('attention', 'attention'),
              ('giving', 'giving'), ('mirror', 'the mirror'), ('friends', 'friends'), ('further', 'someone|further along')]


def fig_eight():
    u = 'ei'
    b = []
    for i, (k, lab) in enumerate(CONDITIONS):
        x = 60 + i * 80
        b.append(f'<circle class="cardm" cx="{x}" cy="96" r="34"/>')
        b.append(_ic(k, x, 96))
        b.append(T(x, 150, f'{i + 1}', 'small faint', 'middle'))
        for j, ln in enumerate(lab.split('|')):
            b.append(T(x, 168 + j * 15, ln, 'small b', 'middle'))
    b.append(f'<path class="stm2" d="M40 206 H640" marker-end="url(#a{u}mu)"/>')
    b.append(T(40, 228, 'only you', 'small'))
    b.append(T(340, 228, 'the daily work', 'small', 'middle'))
    b.append(T(640, 228, 'other people', 'small', 'end'))
    b.append(T(340, 36, 'Eight conditions', 't', 'middle'))
    return svg('0 0 680 244', 'Eight conditions in a row: your wish, a goal, discipline, attention, giving, the mirror, friends on the path and someone further along, running from what only you can supply to what comes from other people', ''.join(b), u)


# ------------------------------------------------------------------ before the yes, after the yes (section 1)
def fig_yes():
    u = 'ye'
    b = []
    days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    angles = (-60, 140, 20, -150, 80, -20, 170)
    for row, (y, lab) in enumerate(((90, 'before the yes: every day a small debate'), (200, 'after the yes: the days line up'))):
        b.append(T(40, y - 44, lab, 'ts'))
        for i, d in enumerate(days):
            x = 80 + i * 86
            b.append(f'<circle class="cardm" cx="{x}" cy="{y}" r="26"/>')
            if row == 0:
                a = math.radians(angles[i])
                b.append(f'<path class="stm2" d="M{x - 14 * math.cos(a):.1f} {y - 14 * math.sin(a):.1f} L{x + 14 * math.cos(a):.1f} {y + 14 * math.sin(a):.1f}" marker-end="url(#a{u}mu)"/>')
            else:
                b.append(f'<path class="hi" d="M{x - 13} {y} H{x + 13}" marker-end="url(#a{u}hi)"/>')
            b.append(T(x, y + 44, d, 'small faint', 'middle'))
    return svg('0 0 680 262', 'A week before a decision, with each day pointing a different way, and a week after it, with every day pointing the same way', ''.join(b), u)


# ------------------------------------------------------------------ fuel and steering (section 2)
def _car(x, y, wheel=True, full=True):
    b = [f'<path class="card" d="M{x - 60} {y} V{y - 22} Q{x - 58} {y - 30} {x - 44} {y - 32} L{x - 26} {y - 52} H{x + 26} L{x + 42} {y - 32} Q{x + 60} {y - 30} {x + 60} {y - 18} V{y} Z"/>',
         f'<path class="stm" d="M{x - 20} {y - 47} H{x + 22} L{x + 33} {y - 32} H{x - 32} Z"/>',
         f'<circle class="knobf" cx="{x - 34}" cy="{y + 2}" r="12"/>', f'<circle class="knobf" cx="{x + 34}" cy="{y + 2}" r="12"/>']
    if wheel:
        b.append(f'<circle class="st" cx="{x + 12}" cy="{y - 38}" r="7"/>')
    gx, gy = x - 6, y - 14
    b.append(f'<rect class="cardm" x="{gx - 14}" y="{gy - 8}" width="28" height="12" rx="3"/>')
    b.append(f'<rect class="{"fhi" if full else "fdo"}" x="{gx - 12}" y="{gy - 6}" width="{24 if full else 4}" height="8" rx="2"/>')
    return ''.join(b)


def fig_cars():
    u = 'cr'
    b = []
    b.append('<path class="stm" d="M30 210 H650"/>')
    b.append(_car(120, 200, wheel=False, full=True))
    b.append(f'<path class="stm2 dash" d="M60 150 C20 110 90 70 130 100 C170 130 210 80 180 60" marker-end="url(#a{u}mu)"/>')
    b.append(T(120, 244, 'fuel, no steering', 'ts', 'middle'))
    b.append(T(120, 262, 'a bomb with a radio', 'small', 'middle'))
    b.append(_car(340, 200, wheel=True, full=False))
    b.append('<path class="cardm" d="M300 120 L320 112 L340 120 L360 112 L380 120 V150 L360 142 L340 150 L320 142 L300 150 Z"/>')
    b.append('<path class="stm" d="M320 112 V142 M340 120 V150 M360 112 V142"/>')
    b.append(T(340, 244, 'a map, no fuel', 'ts', 'middle'))
    b.append(T(340, 262, 'a very well informed parked car', 'small', 'middle'))
    b.append(_car(560, 200, wheel=True, full=True))
    b.append(f'<path class="hi" d="M500 130 C540 110 590 110 630 128" marker-end="url(#a{u}hi)"/>')
    b.append('<path class="st" d="M640 210 V100"/><path class="cardhi" d="M640 100 H664 L656 110 L664 120 H640 Z"/>')
    b.append(T(560, 244, 'both', 'ts', 'middle'))
    b.append(T(560, 262, 'the wish and a goal', 'small', 'middle'))
    return svg('0 0 680 280', 'Three cars: one with fuel and no steering wheel drives in loops, one with a map and an empty tank stays parked, one with both heads for a flag', ''.join(b), u)


# ------------------------------------------------------------------ a goal on a reason (section 2)
def fig_goalreason():
    u = 'gr'
    b = []
    b.append('<rect class="cardhi" x="230" y="40" width="220" height="90" rx="10"/>')
    b.append(T(340, 66, 'the goal', 'ts', 'middle'))
    b.append(T(340, 88, 'plan the family trip', 'small b', 'middle'))
    b.append(T(340, 108, 'short, measurable, real', 'small', 'middle'))
    b.append('<path class="st" d="M340 130 V160"/>')
    b.append('<rect class="card" x="90" y="160" width="500" height="100" rx="12"/>')
    b.append(T(340, 190, 'the reason', 'ts', 'middle'))
    b.append(T(340, 214, 'so the kids grow up feeling that home is a warm place', 'small b', 'middle'))
    b.append(T(340, 236, 'bigger than you, and it keeps going after the excitement', 'small', 'middle'))
    b.append(T(470, 90, 'checks the work', 'small'))
    return svg('0 0 680 276', 'A small goal card sitting on a wider reason card: plan the family trip, so the kids grow up feeling that home is a warm place', ''.join(b), u)


# ------------------------------------------------------------------ five minutes, kept (section 3)
def fig_streak():
    u = 'st5'
    b = []
    b.append(T(340, 26, 'Five minutes, every day', 't', 'middle'))
    days = ('M', 'T', 'W', 'T', 'F', 'S', 'S')
    for i, d in enumerate(days):
        b.append(T(150 + i * 62, 54, d, 'small faint', 'middle'))
    miss = 24
    for r in range(4):
        for c in range(7):
            k = r * 7 + c
            x, y = 126 + c * 62, 64 + r * 52
            b.append(f'<rect class="{"cardm" if k == miss else "card"}" x="{x}" y="{y}" width="48" height="40" rx="6"/>')
            if k != miss:
                b.append(f'<path class="shi" d="M{x + 14} {y + 21} l6 7 l12 -14"/>')
    mx, my = 126 + (miss % 7) * 62, 64 + (miss // 7) * 52
    b.append(f'<path class="leader" d="M{mx + 24} {my + 42} V{my + 62}"/>')
    b.append(T(mx + 24, my + 78, 'a day slips: pick it up tomorrow, no speech', 'small b', 'middle'))
    return svg('0 0 680 310', 'A four-week calendar of five-minute practice ticks with one missed day, and the ticks carrying on the next day', ''.join(b), u)


# ------------------------------------------------------------------ the flashlight on the clamp (section 4)
def fig_clamps():
    u = 'cl'
    b = []
    # head and shoulders
    b.append('<path class="card" d="M150 320 C150 250 200 226 260 220 L270 200 C236 190 222 160 222 128 C222 84 250 58 290 58 C330 58 358 84 358 128 C358 160 344 190 310 200 L320 220 C380 226 430 250 430 320 Z"/>')
    spots = [(262, 116, 'around the eyes'), (290, 176, 'the jaw'), (380, 246, 'a shoulder')]
    for x, y, lab in spots:
        b.append(f'<circle class="warn" cx="{x}" cy="{y}" r="6" fill-opacity=".8"/>')
    b.append('<path class="cone" d="M392 236 L566 172 L566 300 Z"/>')
    b.append('<rect class="card" x="560" y="214" width="80" height="44" rx="8"/>')
    b.append('<path class="card" d="M560 220 L544 206 V266 L560 252 Z"/>')
    b.append('<circle class="fmu2" cx="600" cy="236" r="4"/>')
    b.append(f'<path class="leader" d="M256 112 L130 90"/>')
    b.append(T(124, 86, spots[0][2], 'small b', 'end'))
    b.append(f'<path class="leader" d="M284 180 L130 196"/>')
    b.append(T(124, 200, spots[1][2], 'small b', 'end'))
    b.append(T(380, 290, spots[2][2], 'small b', 'middle'))
    b.append(T(600, 300, 'attention, held', 'small', 'middle'))
    b.append(T(600, 316, 'on one spot, no pushing', 'small', 'middle'))
    return svg('0 0 680 340', 'Head and shoulders with three small clamps marked, at the eyes, the jaw and a shoulder, and a flashlight beam held on the shoulder', ''.join(b), u)


# ------------------------------------------------------------------ three jobs of attention (section 4)
def fig_jobs():
    u = 'jb'
    b = []
    xs = (115, 340, 565)
    # be here
    b.append(person(xs[0], 90, 0.9, 'st'))
    b.append(f'<circle class="ringhi solid" cx="{xs[0]}" cy="130" r="64"/>')
    b.append(T(xs[0], 230, '1. be here', 'ts', 'middle'))
    b.append(T(xs[0], 248, 'in the body, in this room', 'small', 'middle'))
    # let go
    b.append(f'<path class="sdo2" d="M{xs[1] - 48} 100 l8 -8 l8 8 l8 -8 l8 8 l8 -8 l8 8 l8 -8 l8 8 l8 -8 l8 8 l8 -8 l8 8"/>')
    b.append(T(xs[1] + 62, 98, 'held', 'small'))
    b.append(f'<path class="stm2" d="M{xs[1]} 116 V150" marker-end="url(#a{u}mu)"/>')
    b.append(f'<path class="sbe2" d="M{xs[1] - 48} 170 C{xs[1] - 20} 162 {xs[1] + 20} 178 {xs[1] + 48} 170"/>')
    b.append(T(xs[1] + 62, 174, 'let go', 'small'))
    b.append(T(xs[1], 230, '2. let go', 'ts', 'middle'))
    b.append(T(xs[1], 248, 'of what is already held', 'small', 'middle'))
    # don't build new
    b.append(f'<rect class="card" x="{xs[2] - 80}" y="80" width="160" height="100" rx="8"/>')
    for k, ln in enumerate(('take the first step', 'say it now', 'no argument', 'in the shower')):
        b.append(T(xs[2], 108 + k * 18, ln, 'small', 'middle'))
    b.append(T(xs[2], 230, '3. build no new ones', 'ts', 'middle'))
    b.append(T(xs[2], 248, 'the one people forget', 'small', 'middle'))
    return svg('0 0 680 266', 'Three jobs of attention: be here, let go of the tension already held, and build no new tension', ''.join(b), u)


# ------------------------------------------------------------------ what arrives glued together comes apart (section 4)
def fig_apart():
    u = 'ap'
    b = []
    pairs = (('what happened', 'the story about it'), ('a real danger', 'an old fear'), ('what I want', 'what others expect'))
    b.append(T(170, 30, 'arrives glued together', 'ts', 'middle'))
    b.append(T(500, 30, 'with practice', 'ts', 'middle'))
    for i, (a, c) in enumerate(pairs):
        y = 56 + i * 70
        b.append(f'<rect class="card" x="40" y="{y}" width="130" height="48" rx="6"/>')
        b.append(f'<rect class="cardm" x="170" y="{y}" width="130" height="48" rx="6"/>')
        b.append(T(105, y + 29, a, 'small b', 'middle'))
        b.append(T(235, y + 29, c, 'small', 'middle'))
        b.append(f'<rect class="cardhi" x="370" y="{y}" width="130" height="48" rx="6"/>')
        b.append(f'<rect class="cardm" x="530" y="{y}" width="130" height="48" rx="6"/>')
        b.append(T(435, y + 29, a, 'small b', 'middle'))
        b.append(T(595, y + 29, c, 'small', 'middle'))
        b.append(f'<path class="stm dash" d="M515 {y + 6} V{y + 42}"/>')
    b.append(f'<path class="stm2" d="M312 150 H354" marker-end="url(#a{u}mu)"/>')
    return svg('0 0 680 270', 'Three pairs that usually arrive as one block, what happened and the story, a real danger and an old fear, what I want and what others expect, and the same pairs with a gap between them', ''.join(b), u)


# ------------------------------------------------------------------ prayer and the ditch (section 4)
def fig_ditch():
    u = 'dt'
    b = []
    b.append('<path class="card" d="M380 70 C360 70 350 52 366 42 C366 22 396 14 410 30 C424 12 458 18 458 40 C478 40 482 70 460 70 Z"/>')
    for x in (382, 404, 426, 448):
        b.append(f'<path class="water" d="M{x} 82 l-6 16"/>')
    b.append('<path class="stm" d="M30 240 H650"/>')
    b.append('<path class="waterf" d="M200 240 C260 232 360 248 420 240 L640 240 V252 H200 Z"/>')
    b.append('<path class="water" d="M210 246 C280 240 360 252 430 246 C500 240 580 250 640 246"/>')
    b.append(person(150, 152, 1.0, 'st'))
    b.append('<path class="st" d="M168 192 L210 232 M200 236 l18 -4"/>')
    for x in (560, 600, 630):
        b.append(f'<path class="shi" d="M{x} 240 V214 M{x} 224 l-8 -8 M{x} 220 l8 -8"/>')
    b.append(T(420, 120, 'the rain', 'small', 'middle'))
    b.append(T(150, 280, 'and someone digs the ditches', 'small b', 'middle'))
    return svg('0 0 680 296', 'A rain cloud over a field, and a person digging the ditch that carries the water to the plants', ''.join(b), u)


# ------------------------------------------------------------------ the circle widens (section 5)
def fig_circles():
    u = 'ci'
    b = []
    cx, cy = 250, 170
    rings = ((150, 'people who are hard for you'), (112, 'strangers'), (76, 'friends'), (44, 'the people closest to you'))
    for i, (r, lab) in enumerate(rings):
        b.append(f'<circle class="{"ringhi" if i == 0 else "ringhi solid"}" cx="{cx}" cy="{cy}" r="{r}" fill="none"/>')
    b.append(f'<circle class="fhis" cx="{cx}" cy="{cy}" r="44"/>')
    b.append(person(cx, cy - 24, 0.5, 'st'))
    ys = (cy - 150, cy - 112, cy - 76, cy - 44)
    for (r, lab), y in zip(rings, ys):
        b.append(f'<path class="leader" d="M{cx + r * 0.7:.0f} {cy - r * 0.7:.0f} L440 {y + 40:.0f}"/>')
        b.append(T(448, y + 44, lab, 'small b'))
    b.append(f'<path class="hi" d="M100 300 C70 260 70 220 90 196" marker-end="url(#a{u}hi)"/>')
    b.append(T(100, 318, 'one step at a time', 'small', 'middle'))
    return svg('0 0 680 334', 'Concentric circles around one person: the people closest, friends, strangers, and on the outside the people who are hard for you', ''.join(b), u)


# ------------------------------------------------------------------ the rusty lever (section 6)
def fig_lever():
    u = 'lv5'
    b = []
    # tracks
    b.append('<path class="st" d="M40 250 H300 C380 250 440 200 640 140"/>')
    b.append('<path class="st" d="M40 270 H300 C380 270 440 230 640 170"/>')
    b.append('<path class="stm2" d="M300 250 H640 M300 270 H640"/>')
    for x in range(60, 300, 34):
        b.append(f'<path class="stm" d="M{x} 242 V278"/>')
    b.append(T(640, 294, 'the old way', 'small', 'end'))
    b.append(T(640, 126, 'letting it go', 'small b', 'end'))
    # the lever
    b.append('<rect class="card" x="230" y="180" width="70" height="30" rx="4"/>')
    b.append('<path class="st" d="M265 180 L230 90" stroke-width="5"/>')
    b.append('<circle class="knobf" cx="230" cy="88" r="10"/>')
    for x, y in ((240, 118), (251, 146), (258, 163), (246, 132)):
        b.append(f'<circle class="fdo" cx="{x}" cy="{y}" r="3" fill-opacity=".7"/>')
    b.append(f'<path class="hi" d="M220 66 C260 40 310 50 330 80" marker-end="url(#a{u}hi)"/>')
    b.append(T(344, 60, 'rusty, barely moves,', 'small b'))
    b.append(T(344, 76, 'and this one is inside', 'small'))
    return svg('0 0 680 300', 'A rusty railway switch lever by a track that splits: straight on is the old way, the branch is letting it go', ''.join(b), u)


# ------------------------------------------------------------------ the same step away (section 6)
def fig_samestep():
    u = 'ss'
    b = []
    for cx, lab, sub, cls in ((190, 'a clear choice', 'I see it as the best course', 'fhis'), (490, 'a flinch', 'fear decides for me', 'fdos')):
        b.append(f'<circle class="{cls}" cx="{cx}" cy="52" r="34"/>')
        b.append(person(cx, 120, 1.0, 'st'))
        b.append(f'<path class="stm2" d="M{cx + 30} 214 H{cx - 60}" marker-end="url(#a{u}mu)"/>')
        b.append(T(cx, 58, lab, 'small b', 'middle'))
        b.append(T(cx, 250, sub, 'small', 'middle'))
    b.append(T(340, 290, 'From outside the two look identical.', 't', 'middle'))
    return svg('0 0 680 304', 'Two people taking the same step back, one from a clear choice and one from fear, which look the same from outside', ''.join(b), u)


# ------------------------------------------------------------------ after a strong weekend (section 7)
def fig_weekend():
    u = 'wk'
    b = []
    x0, x1, y0, y1 = 80, 640, 40, 240
    b.append(f'<path class="axis" d="M{x0} {y0 - 10} V{y1} H{x1}" />')
    b.append(T(x0 - 10, y0 + 4, 'lit up', 'small', 'end'))
    b.append(T(x1, y1 + 22, 'weeks', 'small', 'end'))
    b.append(f'<path class="stm2" d="M{x0} 200 H140 C150 200 150 60 166 60 C220 60 260 200 330 210 H{x1}"/>')
    b.append(f'<path class="shi" d="M166 60 C220 60 240 100 290 104 C330 108 340 84 380 84 C420 84 440 110 480 108 C520 106 540 80 580 82 H{x1}"/>')
    for x in (290, 400, 510, 620):
        b.append(f'<circle class="fhi" cx="{x}" cy="{"104" if x == 290 else "92"}" r="4"/>')
    b.append(T(400, 70, 'with people you see every week', 'small b', 'middle'))
    b.append(T(400, 230, 'on your own', 'small', 'middle'))
    b.append(T(166, 46, 'a strong weekend', 'small b', 'middle'))
    return svg('0 0 680 270', 'After a strong weekend the lift fades within a couple of weeks on your own, and holds with people you see every week. Illustration, not data', ''.join(b), u)


# ------------------------------------------------------------------ apprentice and smith (section 8)
def fig_smith():
    u = 'sm'
    b = []
    b.append('<path class="stm" d="M30 290 H650"/>')
    # forge
    b.append('<rect class="card" x="60" y="190" width="110" height="100" rx="6"/>')
    b.append('<path class="flame" d="M90 190 C80 170 96 160 100 144 C108 160 118 166 112 190 Z"/>')
    b.append('<path class="flame" d="M122 190 C114 176 126 166 130 154 C138 168 146 174 140 190 Z"/>')
    b.append('<path class="st" d="M70 120 H160 V190 M70 120 V190"/>')
    # anvil
    b.append('<path class="card" d="M290 210 H390 C390 224 372 230 360 232 V260 H380 V290 H300 V260 H320 V232 C300 230 290 220 290 210 Z"/>')
    b.append('<rect class="iron" x="320" y="202" width="40" height="8" rx="3"/>')
    # smith
    b.append(person(250, 160, 1.15, 'st'))
    b.append('<path class="st" d="M268 194 L318 170" stroke-width="3"/><rect class="inkf" x="310" y="160" width="22" height="14" rx="2"/>')
    # apprentice
    b.append(person(480, 176, 0.95, 'st'))
    b.append('<path class="stm dash" d="M468 180 C430 176 390 190 362 202"/>')
    b.append(T(250, 316, 'the smith', 'small b', 'middle'))
    b.append(T(480, 316, 'the apprentice, for years', 'small b', 'middle'))
    b.append(T(580, 110, 'no syllabus,', 'small', 'middle'))
    b.append(T(580, 126, 'just watching how it is done', 'small', 'middle'))
    return svg('0 0 680 330', 'A smith at the anvil with a forge behind, and an apprentice watching from a few steps away', ''.join(b), u)


# ------------------------------------------------------------------ let the emotion pass first (the note)
def fig_emotion():
    u = 'em'
    b = []
    base = 180
    b.append(f'<path class="stm" d="M40 {base} H420"/>')
    b.append(f'<path class="sdo2" d="M60 {base} C100 {base} 110 60 160 60 C210 60 230 {base} 300 {base}"/>')
    b.append(f'<path class="fdos" d="M60 {base} C100 {base} 110 60 160 60 C210 60 230 {base} 300 {base} Z"/>')
    b.append(T(160, 48, 'the emotion', 'small b', 'middle'))
    b.append(T(160, base + 24, 'decide nothing yet', 'small', 'middle'))
    b.append(T(160, base + 40, 'live through it', 'small', 'middle'))
    b.append(f'<circle class="fhi" cx="340" cy="{base}" r="7"/>')
    b.append(T(340, base + 24, 'look again,', 'small b', 'middle'))
    b.append(T(340, base + 40, 'clear head', 'small b', 'middle'))
    b.append(f'<path class="hi" d="M350 {base - 10} C390 {base - 60} 430 {base - 80} 470 {base - 84}" marker-end="url(#a{u}hi)"/>')
    b.append(f'<path class="stm2" d="M350 {base + 4} C390 {base + 30} 430 {base + 44} 470 {base + 48}" marker-end="url(#a{u}mu)"/>')
    b.append(T(480, base - 92, 'mostly gone with the emotion', 'small b'))
    b.append(T(480, base - 76, 'that was growth', 'small'))
    b.append(T(480, base + 52, 'something is still there', 'small b'))
    b.append(T(480, base + 68, 'say so, take it seriously', 'small'))
    return svg('0 0 680 260', 'A disagreement with a wave of emotion: decide nothing until it has passed, then look again with a clear head. Mostly it goes with the emotion; if something stays, say so and take it seriously', ''.join(b), u)


PART2 = [fig_settings, fig_cell, fig_warning, fig_needlove, fig_turn, fig_lamps, fig_hours, fig_mill, fig_paths, fig_border]
PART3 = [fig_eight, fig_yes, fig_cars, fig_goalreason, fig_streak, fig_clamps, fig_jobs, fig_apart, fig_ditch, fig_circles, fig_lever, fig_samestep, fig_weekend, fig_smith, fig_emotion]


# ------------------------------------------------------------------ jokes: extra lines drawn over a figure, in the comic hand Part one uses
def _joke(fig, extra, dh=0):
    s = fig()
    if dh:
        import re
        s = re.sub(r'viewBox="0 0 (\d+) (\d+)"', lambda m: f'viewBox="0 0 {m.group(1)} {int(m.group(2)) + dh}"', s, count=1)
    return s.replace('</svg>', extra + '</svg>')


def J(x, y, s, c='c2', anchor='start'):
    return T(x, y, s, f'dg2 {c}', anchor)


JOKES = {
    'fig_settings': lambda: _joke(fig_settings, J(668, 30, 'someone keeps', 'c2', 'end') + J(668, 48, 'turning this one up', 'c2', 'end')
                                  + '<path class="sdo2" d="M600 56 L578 78" marker-end="url(#asedo)"/>'),
    'fig_cell': lambda: _joke(fig_cell, J(478, 40, 'I could have been an eye.', 'c3') + J(478, 60, 'I chose the liver.', 'c3')),
    'fig_needlove': lambda: _joke(fig_needlove, J(170, 286, '"you complete me"', 'c2', 'middle') + J(510, 286, '"we\'re good"', 'c3', 'middle'), 30),
    'fig_turn': lambda: _joke(fig_turn, J(120, 282, 'meanwhile: pressing the', 'c2', 'middle') + J(120, 300, 'elevator button harder', 'c2', 'middle')),
    'fig_hours': lambda: _joke(fig_hours, '<rect class="card" x="30" y="266" width="290" height="34" rx="10"/>' + J(175, 288, 'Low battery: guarding used 70%', 'c2', 'middle')
                               + '<rect class="card" x="360" y="266" width="290" height="34" rx="10"/>' + J(505, 288, 'Battery: somehow fuller', 'c3', 'middle'), 44),
    'fig_mill': lambda: _joke(fig_mill, J(130, 120, 'MINE', 'c2', 'middle') + J(670, 104, "to the next mill: you're welcome", 'c3', 'end')),
    'fig_border': lambda: _joke(fig_border, J(384, 24, "(don't quote me)", 'c1')),
    'fig_yes': lambda: _joke(fig_yes, J(640, 46, '"maybe Tuesday?"', 'c2', 'end')),
    'fig_streak': lambda: _joke(fig_streak, J(126 + 3 * 62 + 24, 64 + 3 * 52 + 26, 'oops', 'c2', 'middle')),
    'fig_clamps': lambda: _joke(fig_clamps, J(124, 218, '(answering email)', 'c2', 'end')),
    'fig_jobs': lambda: _joke(fig_jobs, J(565, 66, '"and ANOTHER thing"', 'c2', 'middle') + '<path class="sdo2" d="M490 61 H640"/>'),
    'fig_ditch': lambda: _joke(fig_ditch, J(490, 40, '"I did my part"', 'c1')),
    'fig_circles': lambda: _joke(fig_circles, J(448, 84, '(yes, them too)', 'c2')),
    'fig_lever': lambda: _joke(fig_lever, J(344, 100, 'WD-40 not included', 'c2')),
    'fig_weekend': lambda: _joke(fig_weekend, J(262, 150, 'hello, inbox', 'c2')),
    'fig_emotion': lambda: _joke(fig_emotion, J(160, 118, 'write the angry', 'c2', 'middle') + J(160, 138, 'email? not now', 'c2', 'middle')),
}
