"""Illustrations for Part two (inline SVG, theme-aware). Imported by build_html.py.

Uses the drawing helpers from figs2.py, so the hand and the classes match Part one.
CSS_EXTRA holds the few rules these figures need on top of the shared page CSS.
"""
import math

from figs2 import T, arrow, person, svg

CSS_EXTRA = r"""
:root{--night:#1B2440}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--night:#080C18}}
:root[data-theme="dark"]{--night:#080C18}
.chart .night{fill:var(--night);stroke:var(--rule);stroke-width:1.5}
.chart .stp{fill:none;stroke:#E7EBF5;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.chart .mon{fill:#000;fill-opacity:.55;stroke:#E7EBF5;stroke-width:1.2;stroke-opacity:.5;stroke-dasharray:3 4;stroke-linejoin:round}
.chart .eyes{fill:#F2E6A0}
.chart text.pale{fill:#C8D0E6}
.chart .edge{fill:none;stroke:var(--ink);stroke-width:5;stroke-linejoin:round}
.chart .edgesoft{fill:none;stroke:var(--high);stroke-width:2.4;stroke-dasharray:2 8;stroke-linecap:round}
.chart .wave{fill:none;stroke:var(--drifting);stroke-width:2;stroke-linecap:round;opacity:.8}
.chart .handm{fill:var(--card);stroke:var(--ink);stroke-width:1.8;stroke-linejoin:round}
.chart .handd{fill:none;stroke:var(--muted);stroke-width:1.6;stroke-dasharray:5 4}
.chart .brush{fill:none;stroke:var(--driven);stroke-width:3;stroke-linecap:round}
.chart .sight{fill:none;stroke:var(--muted);stroke-width:1.2;stroke-dasharray:2 5}
.chart .mapq{fill:var(--high);fill-opacity:.1;stroke:var(--rule);stroke-width:1}
"""


def _quads(x0, x1, y0, y1):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return mx, my, [
        f'<rect class="q default" x="{x0}" y="{my}" width="{mx - x0}" height="{y1 - my}"/>',
        f'<rect class="q driven" x="{mx}" y="{my}" width="{x1 - mx}" height="{y1 - my}"/>',
        f'<rect class="q drifting" x="{x0}" y="{y0}" width="{mx - x0}" height="{my - y0}"/>',
        f'<rect class="q high" x="{mx}" y="{y0}" width="{x1 - mx}" height="{my - y0}"/>',
    ]


# ------------------------------------------------------------------ the door
def fig_door():
    u = 'dr'
    x0, x1, y0, y1 = 70, 570, 20, 400
    mx, my, b = _quads(x0, x1, y0, y1)
    b.append(f'<circle class="ringm" cx="{mx}" cy="{my}" r="46"/>')
    # a door in the middle of the ring
    b.append(f'<rect class="card" x="{mx - 12}" y="{my - 20}" width="24" height="40" rx="2"/>')
    b.append(f'<circle class="fhi" cx="{mx + 6}" cy="{my + 2}" r="2.6"/>')
    # circling it: a dashed arc that never goes in
    r = 76
    ex, ey = mx + r * math.cos(math.radians(-40)), my + r * math.sin(math.radians(-40))
    sx, sy = mx + r * math.cos(math.radians(40)), my + r * math.sin(math.radians(40))
    b.append(f'<path class="stm dash" d="M{ex:.0f} {ey:.0f} A{r} {r} 0 1 0 {sx:.0f} {sy:.0f}" marker-end="url(#a{u}mu)"/>')
    b.append(T(mx - 86, my - 70, 'circling it for years', 'small', 'end'))
    b.append(T(mx - 86, my - 54, 'a bit less driven, a bit calmer', 'small faint', 'end'))
    # crossing it
    b.append(arrow(u, f'M{mx + 150} {my + 140} C{mx + 90} {my + 90} {mx + 30} {my + 40} {mx} {my} S{mx + 80} {my - 100} {x1 - 40} {y0 + 44}', 'hi', 'climb'))
    b.append(T(mx + 162, my + 146, 'crossing it', 'small b'))
    b.append(T(mx, my + 66, 'the door', 't', 'middle'))
    b.append(T(mx, y1 + 30, 'the middle of the chart, with a name', 'small', 'middle'))
    return svg('0 0 640 440', 'The middle of the chart drawn as a ring with a door in it: some people circle it for years, others cross it', ''.join(b), u)


# ------------------------------------------------------------------ the fist and the water
def fig_fist():
    u = 'fs'
    b = []
    # left: braced
    b.append(person(170, 118, 1.1, 'st', legs=True))
    b.append('<rect class="edge" x="128" y="92" width="84" height="148" rx="14"/>')
    for ox in (44, 296):
        b.append(person(ox, 150, 0.62, 'stm', legs=True))
    b.append(T(170, 34, 'I end here.', 't', 'middle'))
    b.append(T(170, 54, 'Everything past this is other.', 'small', 'middle'))
    b.append(T(170, 284, 'Braced', 't', 'middle'))
    # right: released
    b.append(person(510, 118, 1.1, 'st', legs=True))
    b.append('<ellipse class="edgesoft" cx="510" cy="164" rx="150" ry="86"/>')
    for ox in (402, 618):
        b.append(person(ox, 144, 0.62, 'stm', legs=True))
    for i, wy in enumerate((236, 250, 264)):
        d = f'M{372 + i * 12} {wy} q 12 -9 24 0 t 24 0 t 24 0 t 24 0 t 24 0 t 24 0 t 24 0 t 24 0 t 24 0 t 24 0'
        b.append(f'<path class="wave" d="{d}"/>')
    b.append(T(510, 34, 'The border goes soft.', 't', 'middle'))
    b.append(T(510, 54, 'The water was holding you all along.', 'small', 'middle'))
    b.append(T(510, 292, 'Released', 't', 'middle'))
    b.append('<path class="stm dash" d="M340 40 V276"/>')
    return svg('0 0 680 306', 'Two pictures: a braced person inside a hard outline with everyone else outside it, and a released person whose outline has gone soft', ''.join(b), u)


# ------------------------------------------------------------------ four rooms, one assumption
def fig_rooms():
    u = 'rm'
    b = ['<rect class="room" x="10" y="10" width="660" height="326" rx="14"/>']
    b.append(T(340, 46, 'One quiet assumption under all four rooms', 't', 'middle'))
    b.append(T(340, 68, 'I am a separate thing, and it has to look after itself.', 'small b', 'middle'))
    cards = [
        ('default', 'Default', 'protects', ['braces,', 'complains,', 'plays it safe']),
        ('driven', 'Driven', 'takes', ['goes and gets', 'from outside', 'what it lacks']),
        ('drifting', 'Drifting', 'withdraws', ['steps away from', 'whatever pokes', 'and calls it peace']),
        ('high', 'High agency', 'does it well', ['acts, is honest,', 'is kind, and is', 'mostly unafraid']),
    ]
    for i, (room, name, verb, lines) in enumerate(cards):
        x = 20 + i * 165
        b.append(f'<rect class="q {room}" x="{x}" y="92" width="145" height="190" rx="10"/>')
        b.append(f'<text class="qt {room}" x="{x + 14}" y="124" style="font-size:18px">{name}</text>')
        b.append(T(x + 14, 152, verb, 't'))
        for j, ln in enumerate(lines):
            b.append(T(x + 14, 182 + j * 20, ln, 'small'))
    b.append(T(340, 312, 'The top right is the best version of that thing. The thing is still there.', 'small b', 'middle'))
    return svg('0 0 680 346', 'Four cards, one for each room, under a single assumption: I am a separate thing and must look after myself', ''.join(b), u)


# ------------------------------------------------------------------ the rubber hand
def fig_rubber():
    u = 'rb'
    b = ['<path class="stm" d="M30 190 H650"/>']
    # screen between the real hand and the eyes' view
    b.append('<rect class="card" x="300" y="92" width="12" height="98" rx="2"/>')
    # real hand (hidden)
    b.append('<rect class="handd" x="150" y="148" width="104" height="38" rx="14"/>')
    b.append('<path class="handd" d="M254 160 H266 M254 170 H268 M254 180 H264"/>')
    # rubber hand (in view)
    b.append('<rect class="handm" x="420" y="148" width="104" height="38" rx="14"/>')
    b.append('<path class="handm" d="M524 158 H538 M524 168 H540 M524 178 H536"/>')
    # brushes
    for bx in (232, 502):
        b.append(f'<path class="brush" d="M{bx - 30} 108 L{bx} 146"/>')
        b.append(f'<circle class="fdo" cx="{bx}" cy="146" r="4"/>')
    b.append(T(370, 60, 'both brushes move at the same moment', 'small b', 'middle'))
    b.append(T(202, 214, 'your real hand,', 'small', 'middle'))
    b.append(T(202, 230, 'out of sight', 'small', 'middle'))
    b.append(T(462, 214, 'the rubber hand,', 'small', 'middle'))
    b.append(T(462, 230, 'in plain view', 'small', 'middle'))
    # the eye
    ex, ey = 590, 268
    b.append(f'<path class="st" d="M{ex - 24} {ey} Q{ex} {ey - 18} {ex + 24} {ey} Q{ex} {ey + 18} {ex - 24} {ey} Z"/>')
    b.append(f'<circle class="fmu2" cx="{ex}" cy="{ey}" r="5"/>')
    b.append(f'<path class="sight" d="M{ex - 6} {ey - 14} L544 190"/>')
    b.append(T(ex - 34, ey + 4, 'you look at the rubber one', 'small', 'end'))
    return svg('0 0 680 296', 'The rubber hand illusion: your real hand is hidden behind a screen while a rubber hand in view is stroked in time with it', ''.join(b), u)


# ------------------------------------------------------------------ names on the big map
def fig_names():
    u = 'nm'
    x0, x1, y0, y1 = 70, 570, 20, 440
    w, h = x1 - x0, y1 - y0
    small = w * 0.1
    b = [f'<rect class="mapq" x="{x0}" y="{y0}" width="{w}" height="{h}"/>',
         f'<rect class="frame" x="{x0}" y="{y0}" width="{w}" height="{h}"/>',
         f'<rect class="fillrect high solid" x="{x0}" y="{y1 - small * h / w:.0f}" width="{small:.0f}" height="{small * h / w:.0f}"/>']
    b.append(T(x0 + small + 10, y1 - 26, 'the chart from Part one', 'small b'))
    b.append(T(x0 + small + 10, y1 - 10, 'the small box in the corner', 'small'))
    b.append(f'<text class="qt high" x="{x0 + 16}" y="{y0 + 34}">full human potential</text>')
    names = [('fana', 210, 372), ('samadhi', 310, 326), ('satori', 214, 288), ('the Tao', 380, 276),
             ('nirvana', 296, 214), ('theosis', 470, 228), ('moksha', 360, 158), ("Jacob's ladder", 232, 130),
             ('the Kingdom within', 450, 92), ('stairway to heaven', 468, 164)]
    for s, x, y in names:
        b.append(T(x, y, s, 'small b', 'middle'))
    return svg('0 0 640 480', 'The big map, one thousand by one thousand, with names from different traditions scattered across the far side', ''.join(b), u)


# ------------------------------------------------------------------ the child in the dark
def _coat(ox, cls_body='card'):
    return (f'<path class="{cls_body}" d="M{ox - 4} 66 H{ox + 30} L{ox + 40} 142 H{ox - 14} Z"/>'
            f'<path class="{cls_body}" d="M{ox + 13} 54 V66"/><circle class="{cls_body}" cx="{ox + 13}" cy="50" r="5"/>')


def fig_dark():
    u = 'dk'
    b = []
    for panel, ox, dark in (('l', 14, True), ('r', 366, False)):
        b.append(f'<rect class="{"night" if dark else "room"}" x="{ox}" y="22" width="320" height="216" rx="8"/>')
        sk = 'stp' if dark else 'st'
        # bed and child
        b.append(f'<rect class="{"stp" if dark else "card"}" x="{ox + 108}" y="196" width="104" height="30" rx="4"/>')
        b.append(f'<circle class="{sk}" cx="{ox + 138}" cy="178" r="11"/>')
        b.append(f'<path class="{sk}" d="M{ox + 138} 189 V196"/>')
        if dark:
            # three monsters standing where the coat, the laundry and the chair will be
            b.append(f'<path class="mon" d="M{ox + 44} 142 L{ox + 36} 96 L{ox + 52} 76 L{ox + 48} 56 L{ox + 66} 74 L{ox + 80} 62 L{ox + 78} 96 L{ox + 86} 142 Z"/>')
            b.append(f'<circle class="eyes" cx="{ox + 54}" cy="88" r="4"/><circle class="eyes" cx="{ox + 70}" cy="88" r="4"/>')
            b.append(f'<path class="mon" d="M{ox + 128} 140 Q{ox + 120} 100 {ox + 160} 92 Q{ox + 206} 96 {ox + 200} 140 Z"/>')
            b.append(f'<circle class="eyes" cx="{ox + 150}" cy="116" r="4.5"/><circle class="eyes" cx="{ox + 174}" cy="116" r="4.5"/>')
            b.append(f'<path class="mon" d="M{ox + 244} 142 L{ox + 240} 74 L{ox + 258} 56 L{ox + 268} 78 L{ox + 290} 60 L{ox + 296} 142 Z"/>')
            b.append(f'<circle class="eyes" cx="{ox + 256}" cy="94" r="4"/><circle class="eyes" cx="{ox + 276}" cy="94" r="4"/>')
            b.append(T(ox + 160, 262, 'Lights off: monsters.', 't', 'middle'))
        else:
            b.append(_coat(ox + 40))
            b.append(f'<path class="card" d="M{ox + 128} 140 Q{ox + 126} 118 {ox + 148} 114 Q{ox + 160} 100 {ox + 178} 112 Q{ox + 204} 114 {ox + 200} 140 Z"/>')
            b.append(f'<path class="card" d="M{ox + 244} 142 V104 H{ox + 292} V142 M{ox + 244} 104 V70 M{ox + 244} 70 H{ox + 270} M{ox + 252} 142 V160 M{ox + 286} 142 V160"/>')
            b.append(T(ox + 54, 164, 'coat', 'small', 'middle'))
            b.append(T(ox + 164, 164, 'laundry', 'small', 'middle'))
            b.append(T(ox + 268, 176, 'chair', 'small', 'middle'))
            b.append(T(ox + 160, 262, 'Lights on: the room was empty all along.', 't', 'middle'))
    return svg('0 0 700 280', 'The same room twice: in the dark a child sees monsters, with the light on the monsters are a coat, a pile of laundry and a chair', ''.join(b), u)
