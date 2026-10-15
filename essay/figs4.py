"""Illustrations for the second version of Part two (inline SVG, theme-aware). Imported by build_html.py.

Same drawing helpers and hand as figs2.py and figs3.py. CSS_EXTRA holds the few rules these figures add.
"""
import math

from figs2 import T, arrow, person, svg

CSS_EXTRA = r"""
.chart .chip{fill:var(--card);stroke:var(--ink);stroke-width:2.2;stroke-linejoin:round}
.chart .pin{stroke:var(--ink);stroke-width:2.4;stroke-linecap:round}
.chart .spark{stroke:var(--driven);stroke-width:2.6;stroke-linecap:round}
.chart .orbit{fill:none;stroke:var(--drifting);stroke-width:1.6;stroke-dasharray:3 4}
.chart .earth{fill:var(--drifting);fill-opacity:.3;stroke:var(--drifting);stroke-width:1.8}
.chart .sun{fill:#F2C14E;stroke:var(--ink);stroke-width:1.4}
.chart .gal{fill:none;stroke:var(--high);stroke-width:2.2;stroke-linecap:round}
.chart .starp{fill:var(--ink)}
.chart .thread{fill:none;stroke:var(--high);stroke-width:3;stroke-linecap:round;stroke-dasharray:1 7}
.chart .life{fill:none;stroke:var(--ink);stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.chart .scale{stroke:var(--ink);stroke-width:2;stroke-linecap:round}
.chart .tick{stroke:var(--ink);stroke-width:2;stroke-linecap:round}
.chart .braceln{fill:none;stroke:var(--muted);stroke-width:1.6;stroke-linecap:round}
.chart .zoneb{fill:var(--high);fill-opacity:.1}
.chart .zones{fill:var(--drifting);fill-opacity:.1}
.chart .num{font-family:var(--display);font-weight:800;font-size:19px;fill:var(--ink)}
.chart .cell{fill:var(--card);stroke:var(--ink);stroke-width:1.8}
.chart .wallh{fill:none;stroke:var(--ink);stroke-width:9;stroke-linejoin:round}
.chart .wallt{fill:none;stroke:var(--high);stroke-width:2.2;stroke-dasharray:3 6;stroke-linecap:round}
.chart .hnd-o{fill:none;stroke:var(--ink);stroke-width:42;stroke-linecap:round;stroke-linejoin:round}
.chart .hnd-i{fill:none;stroke:var(--card);stroke-width:36;stroke-linecap:round;stroke-linejoin:round}
.chart .hnd-p{fill:var(--card);stroke:var(--ink);stroke-width:3;stroke-linejoin:round}
.chart .hnd-t{fill:var(--driven);fill-opacity:.16;stroke:none}
.chart .hnd-r{fill:none;stroke:var(--driven);stroke-width:2.4;stroke-linecap:round;stroke-dasharray:2 6}
.chart .hnd-h{fill:none;stroke:var(--driven);stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}
.tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table.rosetta{border-collapse:collapse;min-width:42rem;width:100%;font-size:.76rem;line-height:1.42;background:var(--card)}
table.rosetta th,table.rosetta td{border:1px solid var(--rule);padding:.5rem .55rem;vertical-align:top;text-align:left}
table.rosetta thead th{font-family:var(--mono);font-size:.74rem;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);background:var(--paper)}
table.rosetta tbody th{font-family:var(--display);font-weight:700;font-size:.86rem;color:var(--ink);background:var(--paper);min-width:6.5rem}
"""

MINUS = '−'


# ------------------------------------------------------------------ two views
def fig_views():
    u = 'vw'
    b = []
    b.append(T(170, 28, 'View one', 't', 'middle'))
    b.append(T(170, 46, 'many separate things', 'small', 'middle'))
    for i in range(2):
        for j in range(3):
            x, y = 50 + j * 100, 64 + i * 92
            b.append(f'<rect class="cell" x="{x}" y="{y}" width="80" height="80" rx="10"/>')
            b.append(person(x + 40, y + 16, 0.5, 'st', legs=True))
    for k, ln in enumerate(('Matter first.', 'The mind is what a brain does.', 'When the brain stops, so do you.')):
        b.append(T(170, 294 + k * 17, ln, 'small', 'middle'))
    b.append('<path class="stm dash" d="M340 24 V340"/>')
    cx, cy = 510, 168
    b.append(T(510, 28, 'View two', 't', 'middle'))
    b.append(T(510, 46, 'one whole, seen from many places', 'small', 'middle'))
    b.append(f'<ellipse class="edgesoft" cx="{cx}" cy="{cy + 8}" rx="150" ry="100"/>')
    b.append(f'<circle class="fhi" cx="{cx}" cy="{cy + 8}" r="14"/>')
    pts = [(-100, -34), (-52, 56), (50, 62), (104, -28), (-30, -64), (46, -60)]
    for dx, dy in pts:
        b.append(f'<path class="stm dash" d="M{cx} {cy + 8} L{cx + dx} {cy + 8 + dy}"/>')
        b.append(person(cx + dx, cy + 8 + dy - 22, 0.42, 'st', legs=True))
    for k, ln in enumerate(('Experience first.', 'Separation is how it looks', 'from one position.')):
        b.append(T(510, 294 + k * 17, ln, 'small', 'middle'))
    return svg('0 0 680 352', 'Two views: many separate things inside their own outlines, and one whole seen from many places', ''.join(b), u)


# ------------------------------------------------------------------ one machine, many windows
def fig_cpu():
    u = 'cp'
    b = []
    b.append('<rect class="screen" x="70" y="20" width="540" height="150" rx="10"/>')
    b.append('<rect class="card" x="100" y="48" width="130" height="86" rx="6"/>')
    b.append(T(165, 98, 'me', 't', 'middle'))
    b.append('<rect class="card" x="450" y="48" width="130" height="86" rx="6"/>')
    b.append(T(515, 98, 'you', 't', 'middle'))
    b.append(f'<path class="stm" d="M240 91 H440" marker-end="url(#a{u}mu)" marker-start="url(#a{u}mu)"/>')
    b.append(T(340, 80, 'far apart on the screen', 'small', 'middle'))
    # CPU
    b.append('<rect class="chip" x="270" y="226" width="140" height="70" rx="8"/>')
    for k in range(5):
        x = 290 + k * 25
        b.append(f'<path class="pin" d="M{x} 226 V214 M{x} 296 V308"/>')
    b.append(T(340, 258, 'one processor', 't', 'middle'))
    b.append(T(340, 278, 'no distance in here', 'small', 'middle'))
    b.append(f'<path class="hi" d="M165 138 C165 190 280 190 300 222" marker-end="url(#a{u}hi)"/>')
    b.append(f'<path class="hi" d="M515 138 C515 190 400 190 380 222" marker-end="url(#a{u}hi)"/>')
    b.append(T(110, 206, 'private memory,', 'small', 'middle'))
    b.append(T(110, 222, 'walls enforced', 'small', 'middle'))
    b.append(T(570, 206, 'the same chips,', 'small', 'middle'))
    b.append(T(570, 222, 'underneath', 'small', 'middle'))
    return svg('0 0 680 320', 'Two windows far apart on a screen are both computed by the same processor, where that distance does not exist', ''.join(b), u)


# ------------------------------------------------------------------ the fingers
def fig_fingers():
    u = 'fg'
    b = []
    fingers = [((275, 270), (262, 178)), ((321, 270), (316, 152)), ((367, 270), (372, 126)), ((413, 270), (416, 142)), ((428, 322), (488, 272))]
    for (x0, y0), (x1, y1) in fingers:
        b.append(f'<path class="hnd-o" d="M{x0} {y0} L{x1} {y1}"/>')
    b.append('<rect class="hnd-p" x="245" y="246" width="190" height="168" rx="48"/>')
    for (x0, y0), (x1, y1) in fingers:
        b.append(f'<path class="hnd-i" d="M{x0} {y0} L{x1} {y1}"/>')
    # the hand takes the hit: tint and ripples in the palm
    b.append('<rect class="hnd-t" x="249" y="250" width="182" height="160" rx="44"/>')
    for r in (34, 62, 90):
        b.append(f'<path class="hnd-r" d="M{340 - r} 330 A{r} {r * 0.72:.0f} 0 0 0 {340 + r} 330"/>')
    # the two fingers pressing and rubbing
    b.append('<path class="hnd-h" d="M394 130 l5 10 l-9 9 l9 9 l-9 9 l9 9 l-5 10"/>')
    for ang in (-150, -115, -90, -65, -30):
        x2 = 394 + 26 * math.cos(math.radians(ang))
        y2 = 108 + 26 * math.sin(math.radians(ang))
        x1 = 394 + 14 * math.cos(math.radians(ang))
        y1 = 108 + 14 * math.sin(math.radians(ang))
        b.append(f'<path class="hnd-h" d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}"/>')
    # the harm travels down to the hand
    b.append(f'<path class="hnd-h dash" d="M394 188 V276" marker-end="url(#a{u}do)"/>')
    # labels
    b.append(f'<path class="leader" d="M438 116 L424 122"/>')
    b.append(T(446, 112, 'two fingers', 'small b'))
    b.append(T(446, 128, 'fighting', 'small b'))
    b.append(f'<path class="leader" d="M236 330 L252 330"/>')
    b.append(T(228, 326, 'the whole hand', 'small b', 'end'))
    b.append(T(228, 342, 'feels it', 'small b', 'end'))
    b.append(T(340, 452, 'There was only ever one hand.', 't', 'middle'))
    return svg('0 0 680 472', 'One open hand in which two neighbouring fingers press and rub against each other, with the harm travelling down into the palm, which is the one hand they both belong to', ''.join(b), u)


# ------------------------------------------------------------------ lives and the thread between
def fig_lives():
    u = 'lv'
    base = 236
    b = []
    b.append('<path class="stm dash" d="M30 60 H640"/>')
    b.append(T(640, 50, 'the experience of unity', 'small b', 'end'))
    humps = [(50, 170, 176), (210, 330, 140), (370, 490, 100)]
    for x0, x1, top in humps:
        mid = (x0 + x1) / 2
        b.append(f'<path class="life" d="M{x0} {base} C{x0 + 14} {base - 10} {mid - 30} {top} {mid} {top} C{mid + 30} {top} {x1 - 14} {base - 10} {x1} {base}"/>')
    b.append(f'<path class="life" d="M530 {base} C560 {base - 30} 560 80 600 62"/>')
    b.append('<circle class="fhi" cx="604" cy="60" r="7"/>')
    b.append(f'<path class="thread" d="M20 {base + 16} H640"/>')
    for x in (110, 270, 430):
        b.append(T(x, base - 30, 'life', 'small', 'middle'))
    b.append(T(578, base - 30, 'life', 'small', 'middle'))
    for x in (190, 350, 510):
        b.append(T(x, base + 36, 'between', 'small faint', 'middle'))
    b.append(T(430, 78, 'most of us stop', 'small', 'middle'))
    b.append(T(430, 94, 'short of the top', 'small', 'middle'))
    b.append(T(330, base + 58, 'the thread that carries over: the soul', 'small b', 'middle'))
    return svg('0 0 680 306', 'Several lives rising toward the experience of unity, with a thread running through the gaps between them', ''.join(b), u)


# ------------------------------------------------------------------ the arrow, -4 to +4
def _runner(x, y):
    return (f'<circle class="st" cx="{x}" cy="{y}" r="7"/>'
            f'<path class="st" d="M{x} {y + 7} L{x + 4} {y + 28} M{x + 2} {y + 14} L{x + 18} {y + 10} M{x + 2} {y + 14} L{x - 14} {y + 22} '
            f'M{x + 4} {y + 28} L{x + 20} {y + 36} M{x + 4} {y + 28} L{x - 10} {y + 40}"/>')


def _bike(x, y):
    return (f'<circle class="st" cx="{x - 16}" cy="{y + 22}" r="12"/><circle class="st" cx="{x + 16}" cy="{y + 22}" r="12"/>'
            f'<path class="st" d="M{x - 16} {y + 22} L{x - 2} {y + 6} L{x + 16} {y + 22} M{x - 2} {y + 6} L{x + 8} {y + 6} M{x - 2} {y + 6} L{x - 6} {y - 4}"/>')


def _car(x, y):
    return (f'<path class="card" d="M{x - 30} {y + 30} V{y + 16} Q{x - 28} {y + 8} {x - 18} {y + 6} L{x - 10} {y - 4} H{x + 12} L{x + 20} {y + 6} Q{x + 30} {y + 8} {x + 32} {y + 16} V{y + 30} Z"/>'
            f'<circle class="fmu2" cx="{x - 16}" cy="{y + 32}" r="7"/><circle class="fmu2" cx="{x + 18}" cy="{y + 32}" r="7"/>')


def _plane(x, y):
    return (f'<path class="card" d="M{x - 30} {y + 12} L{x + 22} {y + 10} Q{x + 34} {y + 12} {x + 22} {y + 16} L{x - 30} {y + 18} Z"/>'
            f'<path class="card" d="M{x - 4} {y + 12} L{x - 16} {y - 8} L{x - 6} {y - 8} L{x + 12} {y + 12} Z"/>'
            f'<path class="card" d="M{x - 4} {y + 18} L{x - 16} {y + 38} L{x - 6} {y + 38} L{x + 12} {y + 18} Z"/>'
            f'<path class="card" d="M{x - 30} {y + 12} L{x - 36} {y} L{x - 28} {y} L{x - 20} {y + 12} Z"/>')


def _orbit(x, y):
    return (f'<circle class="earth" cx="{x}" cy="{y + 18}" r="16"/>'
            f'<ellipse class="orbit" cx="{x}" cy="{y + 18}" rx="32" ry="14" transform="rotate(-20 {x} {y + 18})"/>'
            f'<rect class="card" x="{x + 22}" y="{y + 2}" width="12" height="8" rx="1.5" transform="rotate(-20 {x + 28} {y + 6})"/>')


def _rocket(x, y):
    return (f'<path class="card" d="M{x} {y - 6} Q{x + 10} {y + 10} {x + 8} {y + 30} H{x - 8} Q{x - 10} {y + 10} {x} {y - 6} Z"/>'
            f'<path class="card" d="M{x - 8} {y + 22} L{x - 16} {y + 34} L{x - 8} {y + 30} Z M{x + 8} {y + 22} L{x + 16} {y + 34} L{x + 8} {y + 30} Z"/>'
            f'<circle class="fhi" cx="{x}" cy="{y + 12}" r="3.5"/>'
            f'<path class="spark" d="M{x - 3} {y + 34} L{x - 5} {y + 46} M{x + 3} {y + 34} L{x + 5} {y + 46}"/>')


def _solar(x, y):
    o = [f'<circle class="sun" cx="{x}" cy="{y + 20}" r="9"/>']
    for r, a in ((16, 30), (24, 140), (32, 250)):
        o.append(f'<circle class="orbit" cx="{x}" cy="{y + 20}" r="{r}"/>')
        o.append(f'<circle class="starp" cx="{x + r * math.cos(math.radians(a)):.1f}" cy="{y + 20 + r * math.sin(math.radians(a)):.1f}" r="2.6"/>')
    return ''.join(o)


def _galaxy(x, y):
    cy = y + 20
    d1 = f'M{x} {cy} C{x + 8} {cy - 14} {x + 28} {cy - 10} {x + 30} {cy + 4} C{x + 30} {cy + 20} {x + 6} {cy + 28} {x - 14} {cy + 20}'
    d2 = f'M{x} {cy} C{x - 8} {cy + 14} {x - 28} {cy + 10} {x - 30} {cy - 4} C{x - 30} {cy - 20} {x - 6} {cy - 28} {x + 14} {cy - 20}'
    return f'<path class="gal" d="{d1}"/><path class="gal" d="{d2}"/><circle class="sun" cx="{x}" cy="{cy}" r="4"/>'


def _universe(x, y):
    pts = [(-30, 6), (-18, -14), (-4, 12), (10, -8), (24, 10), (30, -12), (-26, 28), (0, 32), (18, 30), (-10, 0), (6, 14)]
    o = ''.join(f'<circle class="starp" cx="{x + dx}" cy="{y + 20 + dy - 6}" r="2.2"/>' for dx, dy in pts)
    links = [(0, 1), (1, 3), (3, 5), (2, 4), (2, 9), (9, 1), (4, 10), (10, 3), (6, 2), (7, 10), (8, 4)]
    o += ''.join(f'<path class="stm" d="M{x + pts[i][0]} {y + 14 + pts[i][1]} L{x + pts[j][0]} {y + 14 + pts[j][1]}"/>' for i, j in links)
    return o


def fig_arrow():
    u = 'ar'
    x0, step, ay = 90, 90, 250
    pos = {n: x0 + (n + 4) * step for n in range(-4, 5)}
    top, bottom = 30, ay + 140
    b = []
    b.append(f'<rect class="zones" x="{pos[-4] - 44}" y="{top}" width="{pos[1] - pos[-4] + 44}" height="{bottom - top}" rx="8"/>')
    b.append(f'<rect class="zoneb" x="{pos[1]}" y="{top}" width="{pos[4] - pos[1] + 62}" height="{bottom - top}" rx="8"/>')
    b.append(T(pos[-4] - 30, 56, 'inside the small square', 't'))
    b.append(T(pos[1] + 14, 56, 'in the zoomed out map', 't'))
    b.append(f'<path class="scale" d="M{pos[-4] - 30} {ay} H{pos[4] + 50}" marker-end="url(#a{u}ink)"/>')
    for n in range(-4, 5):
        x = pos[n]
        b.append(f'<path class="tick" d="M{x} {ay - 8} V{ay + 8}"/>')
        label = ('+' + str(n)) if n > 0 else (MINUS + str(-n) if n < 0 else '0')
        b.append(f'<text class="num" x="{x}" y="{ay + 34}" text-anchor="middle">{label}</text>')
    b.append(_runner(pos[-4] + 4, 150))
    b.append(_bike(pos[-3] + 2, 160))
    b.append(_car(pos[-2], 158))
    b.append(_plane(pos[-1] + 14, 156))
    b.append(_orbit(pos[0] + 26, 154))
    b.append(_rocket(pos[1] + 10, 134))
    b.append(_solar(pos[2], 152))
    b.append(_galaxy(pos[3], 152))
    b.append(_universe(pos[4], 152))
    cap = [(pos[-4] + 4, 'run'), (pos[-3] + 2, 'ride'), (pos[-2], 'drive'), (pos[-1] + 14, 'fly'), (pos[0] + 26, 'orbit'),
           (pos[1] + 10, 'escape'), (pos[2], 'solar system'), (pos[3], 'galaxy'), (pos[4], 'universe')]
    for x, sx in cap:
        b.append(T(x, ay + 62, sx, 'small b', 'middle'))
    notes = [(pos[-3], ('the ground', 'decides where', 'you go')), (pos[-1] - 6, ('the air:', 'any point', 'on the globe')),
             (pos[0] + 28, ('in space,', 'still under', "Earth's gravity")),
             (pos[1] + 22, ('11.2 km/s', 'leaves', 'the Earth')), (pos[2] + 14, ('16.7 km/s', 'leaves', 'the Sun')),
             (pos[3] + 12, ('550 km/s', 'leaves', 'the galaxy')), (pos[4] + 6, ('no pull', 'left to', 'leave'))]
    for x, lines in notes:
        for k, ln in enumerate(lines):
            b.append(T(x, ay + 90 + k * 16, ln, 'small', 'middle'))
    b.append(f'<path class="stm dash" d="M{pos[0]} 84 V{ay - 12}"/>')
    b.append(T(pos[0] - 6, 92, 'the door', 'small b', 'end'))
    b.append(f'<path class="stm dash" d="M{pos[1]} 84 V{ay - 12}"/>')
    b.append(T(pos[1] + 6, 92, 'top right corner', 'small b', 'start'))
    b.append(T(pos[4] + 66, ay - 4, 'birth', 't', 'start'))
    b.append(T(pos[4] + 66, ay + 14, 'and then?', 'small', 'start'))
    return svg('0 0 940 412', 'The arrow of consciousness from minus four to plus four, drawn as speed and freedom of movement: run, ride, drive, fly, orbit, escape, solar system, galaxy, universe', ''.join(b), u)


# ------------------------------------------------------------------ orbit versus escape
def fig_escape():
    u = 'es'
    k = 36
    x0 = 130
    b = []
    b.append(T(x0 - 14, 66, 'orbit', 't', 'end'))
    b.append(f'<rect class="fillrect drifting solid" x="{x0}" y="42" width="{7.7 * k:.0f}" height="34" rx="4"/>')
    b.append(T(x0 + 7.7 * k + 10, 64, '7.7 km/s', 'small b'))
    b.append(T(x0 + 7.7 * k + 10, 82, 'falls around the Earth, for ever', 'small'))
    b.append(f'<path class="braceln" d="M{x0 + 7.7 * k:.0f} 98 V104 H{x0 + 10.8 * k:.0f} V98"/>')
    b.append(T(x0 + (7.7 + 10.8) * k / 2, 124, 'about 40 percent more speed', 'small b', 'middle'))
    b.append(T(x0 - 14, 178, 'escape', 't', 'end'))
    b.append(f'<rect class="fillrect high solid" x="{x0}" y="154" width="{10.8 * k:.0f}" height="34" rx="4"/>')
    b.append(T(x0 + 10.8 * k + 10, 176, '10.8 km/s', 'small b'))
    b.append(T(x0 + 10.8 * k + 10, 194, 'never comes back', 'small'))
    b.append(T(350, 228, 'at the height of the International Space Station', 'small', 'middle'))
    return svg('0 0 700 244', 'At the height of the space station, orbital speed is about 7.7 kilometers per second and escape speed about 10.8, roughly 40 percent more', ''.join(b), u)


# ------------------------------------------------------------------ the wall, held and let go
def fig_wall():
    u = 'wl'
    b = []
    # left: the wall held up
    b.append('<g transform="translate(40 0)">')
    b.append('<rect class="wallh" x="108" y="146" width="124" height="126" rx="20"/>')
    b.append(person(170, 172, 1.0, 'st', legs=True))
    for y, lab in ((172, 'tension'), (204, 'resistance'), (236, 'non-acceptance')):
        b.append(f'<path class="leader" d="M90 {y} L108 {y}"/>')
        b.append(f'<circle class="dot ink" cx="108" cy="{y}" r="3.2"/>')
        b.append(T(84, y + 4, lab, 'small b', 'end'))
    b.append(T(170, 300, 'I end here.', 't', 'middle'))
    b.append('</g>')
    # centre: the BE axis
    b.append(f'<path class="hi" d="M340 300 V46" marker-end="url(#a{u}hi)"/>')
    b.append(T(352, 40, 'released', 'small b'))
    b.append(T(352, 300, 'braced', 'small b'))
    b.append(T(326, 176, 'BE', 'big3', 'end'))
    # right: the same person, less wall, higher
    b.append('<ellipse class="wallt" cx="505" cy="108" rx="66" ry="72"/>')
    b.append(person(505, 66, 1.0, 'st', legs=True))
    b.append(T(505, 204, 'The same person, less wall.', 't', 'middle'))
    b.append(T(505, 224, 'Tension, resistance and non-acceptance let go.', 'small', 'middle'))
    return svg('0 0 680 320', 'On the left a person inside a thick wall labelled tension, resistance and non-acceptance, low on the BE axis; on the right the same person with only a thin dotted wall, higher on the axis', ''.join(b), u)


# ------------------------------------------------------------------ the chain of steps
def fig_chain():
    u = 'ch'
    b = []
    b.append('<rect class="cardhi" x="20" y="10" width="640" height="76" rx="12"/>')
    b.append(T(40, 36, 'The axiom', 't'))
    b.append(T(40, 56, 'clause 1: we are one  /  clause 2: the whole experiences separation', 'small'))
    b.append(T(40, 74, 'clause 3: the separation ends', 'small'))
    steps = [
        ('Separation is a way of looking', 'the whole looks at itself from positions', ['from clauses 1 and 2']),
        ('The wall is held by the body', 'what keeps a way of looking in place', ['from step 1,', 'plus an observation']),
        ('One life is too short', 'most do not finish, so the return takes longer', ['from clause 3,', 'and step 2']),
        ('Something carries over', 'a run that long needs a thread: the soul', ['from step 3']),
        ('Karma, or the fingers', 'nobody else to harm; the thread meets what it did', ['from clause 1,', 'carried by step 4']),
        ('Letting go, and repair', 'loosen the wall, mend the fingers', ['from steps 2 and 5']),
        ('The return, in stages', 'a gradual road with an end, in stages', ['from steps 3 and 6,', 'and clause 3']),
    ]
    y0, h, gap = 112, 62, 24
    prev_bottom = 86
    for i, (title, because, tags) in enumerate(steps):
        y = y0 + i * (h + gap)
        b.append(f'<path class="st" d="M245 {prev_bottom + 2} V{y - 3}" marker-end="url(#a{u}ink)"/>')
        b.append(f'<rect class="card" x="20" y="{y}" width="450" height="{h}" rx="10"/>')
        b.append(T(40, y + 41, str(i + 1), 'big3'))
        b.append(T(76, y + 28, title, 't'))
        b.append(T(76, y + 48, because, 'small'))
        for k, tg in enumerate(tags):
            b.append(T(490, y + 28 + k * 17, tg, 'small b'))
        prev_bottom = y + h
    return svg('0 0 680 %d' % (prev_bottom + 14), 'A chain of seven steps, each following from the one before and from a clause of the axiom: separation is a way of looking, the wall is held by the body, one life is too short, something carries over, karma, letting go and repair, and the return in stages', ''.join(b), u)


# ------------------------------------------------------------------ the table: same structure, different words
ROSETTA_COLS = ['Buddhism', 'Jainism', 'Judaism', 'Christianity', 'Islam']
ROSETTA_ROWS = [
    ('The one whole', [
        ('', 'Dependent arising: nothing stands alone. Huayan: a net of jewels, each reflecting all the others.'),
        ('', 'Countless souls, alike in nature. \u201cSouls render service to one another.\u201d'),
        ('', 'Zohar: the Torah, the Holy One and Israel are one. Chabad: from God\u2019s side the world has no separate existence.'),
        ('', 'One body in Christ. \u201cThat God may be all in all\u201d (1 Cor 15:28). The mystics speak of union with God.'),
        ('', '\u201cWherever you turn, there is the face of God\u201d (2:115). Ibn Arabi: all things are \u201cHe/not He\u201d (Chittick\u2019s rendering).'),
    ]),
    ('The veil', [
        ('', 'Ignorance (avidya). The belief in a permanent self is the first fetter to fall.'),
        ('', 'Karma veils the soul\u2019s own knowledge, like clouds over the sun.'),
        ('', 'God\u2019s hidden face, said by the Baal Shem Tov to be only apparent. The shattered vessels.'),
        ('', '\u201cAlienated from the life of God because of the ignorance that is in them\u201d (Eph 4:18, ESV). The prince who forgets, in the Hymn of the Pearl.'),
        ('', 'The forgotten covenant: \u201cAm I not your Lord?\u201d (7:172).'),
    ]),
    ('The return', [
        ('', 'Nirvana: the ending of ignorance and craving. In Mahayana, the bodhisattva comes back to the marketplace.'),
        ('', 'Moksha: the soul freed from karma, knowing all things.'),
        ('', 'Tikkun, the repair. Devekut, cleaving to God. \u201cOn that day the LORD will be one and his name one\u201d (Zech 14:9, ESV).'),
        ('', 'Origen and Gregory of Nyssa read 1 Cor 15:28 as the restoration of all things.'),
        ('', '\u201cTo Him we return\u201d (2:156). Sufis: fana, the passing away of the self, then baqa, subsistence in God and living on in the world.'),
    ]),
    ('What continues', [
        ('', 'Rebirth without a fixed soul, like a flame passed from lamp to lamp.'),
        ('', 'The soul passes through four realms. Fourteen stages of growth.'),
        ('', 'Gilgul in the Zohar and Luria. A limited time in Gehinnom.'),
        ('', 'Purgatory in Catholic teaching. Gregory of Nyssa\u2019s endless progress after death.'),
        ('', 'The barzakh. Mulla Sadra: the soul keeps developing after death.'),
    ]),
    ('What you do to another', [
        ('', 'Shantideva: the limbs are many, the body one, and beings are alike in wanting happiness.'),
        ('', 'Non-harm grounded in the equality of souls. \u201cI forgive all beings.\u201d'),
        ('', 'All Israel are responsible for one another (Shevuot 39a). Tanya: Jewish souls share one root.'),
        ('', '\u201cIf one member suffers, all suffer together\u201d (1 Cor 12:26). \u201cSaul, why do you persecute me?\u201d'),
        ('', '\u201cIf you do good, you do good for yourselves\u201d (17:7, Sahih International). The believers are like one body.'),
    ]),
    ('Letting go', [
        ('', 'Relinquishing, in the breath practice (MN 118). The second pain you add (SN 36.6). Dropping off body and mind (Dogen).'),
        ('', 'Samayika, equanimity. Kayotsarga, giving up attachment to the body.'),
        ('', 'Bittul, nullifying the self. Praise and insult feel the same.'),
        ('', 'Kenosis, \u201che emptied himself.\u201d Eckhart\u2019s letting go. The stillness of the hesychasts.'),
        ('', 'Islam means surrender (3:83). \u201cI become his hearing and his sight\u201d (Bukhari).'),
    ]),
]


def rosetta_html():
    import html as _h
    head = '<th scope="col"></th>' + ''.join(f'<th scope="col">{_h.escape(c)}</th>' for c in ROSETTA_COLS)
    rows = []
    for label, cells in ROSETTA_ROWS:
        tds = ''.join(f'<td class="{cls}">{_h.escape(txt)}</td>' if cls else f'<td>{_h.escape(txt)}</td>' for cls, txt in cells)
        rows.append(f'<tr><th scope="row">{_h.escape(label)}</th>{tds}</tr>')
    return f'<div class="tscroll"><table class="rosetta"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
