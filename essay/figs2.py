"""More illustrations for the essay page (inline SVG, theme-aware). Imported by build_html.py."""
import html
import math


def esc(s):
    return html.escape(s, quote=False)


def markers(uid):
    out = ''
    for name, cls in (('ink', 'mk-ink'), ('hi', 'mk-hi'), ('mu', 'mk-mu'), ('do', 'mk-do')):
        out += (f'<marker id="a{uid}{name}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                f'<path class="{cls}" d="M1.5 1.5 L8.5 5 L1.5 8.5" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker>')
    return out


def svg(vb, label, body, uid):
    return (f'<svg class="chart ill" viewBox="{vb}" role="img" aria-label="{html.escape(label)}">'
            f'<defs>{markers(uid)}</defs>{body}</svg>')


def T(x, y, s, cls='', anchor='start'):
    c = f' class="{cls}"' if cls else ''
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text{c} x="{x}" y="{y}"{a}>{esc(s)}</text>'


def arrow(uid, d, kind='ink', cls='st'):
    return f'<path class="{cls}" d="{d}" marker-end="url(#a{uid}{kind})"/>'


def person(x, y, s=1.0, cls='st', legs=True):
    """Stick person; (x, y) is the centre of the head."""
    r = 11 * s
    p = [f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r:.1f}"/>',
         f'<path class="{cls}" d="M{x} {y + r:.1f} V{y + 52 * s:.1f} M{x} {y + 22 * s:.1f} L{x - 18 * s:.1f} {y + 40 * s:.1f} M{x} {y + 22 * s:.1f} L{x + 18 * s:.1f} {y + 40 * s:.1f}"/>']
    if legs:
        p.append(f'<path class="{cls}" d="M{x} {y + 52 * s:.1f} L{x - 14 * s:.1f} {y + 86 * s:.1f} M{x} {y + 52 * s:.1f} L{x + 14 * s:.1f} {y + 86 * s:.1f}"/>')
    return ''.join(p)


# ------------------------------------------------------------------ DO
def fig_wheel():
    u = 'wh'
    cx, cy = 170, 150
    b = [f'<circle class="rim" cx="{cx}" cy="{cy}" r="96"/>',
         f'<path class="spoke" d="M{cx - 96} {cy} H{cx + 96} M{cx} {cy} V{cy + 96}"/>',
         f'<circle class="fmu2" cx="{cx}" cy="{cy}" r="26"/>']
    for ang in (-150, -30):
        hx = cx + 96 * math.cos(math.radians(ang))
        hy = cy + 96 * math.sin(math.radians(ang))
        b.append(f'<circle class="card" cx="{hx:.1f}" cy="{hy:.1f}" r="16"/>')
    for ang, y, s in ((-40, 80, 'How often do you start things?'), (0, 150, 'How much effort will you put in?'), (40, 220, 'How much do you actually finish?')):
        px = cx + 96 * math.cos(math.radians(ang))
        py = cy + 96 * math.sin(math.radians(ang))
        b.append(f'<path class="stm dash" d="M{px:.1f} {py:.1f} L318 {y}"/>')
        b.append(f'<circle class="fhi" cx="318" cy="{y}" r="4"/>')
        b.append(T(332, y + 4, s))
    b.append(T(cx, 284, 'Front seat or back seat?', 't', 'middle'))
    return svg('0 0 600 300', 'A steering wheel with three questions: how often you start things, how much effort you put in, how much you finish', ''.join(b), u)


def icons_html():
    def wrap(inner, label):
        return (f'<figure class="ic"><svg class="chart icon" viewBox="0 0 64 64" role="img" aria-label="{label}">{inner}</svg>'
                f'<figcaption>{label}</figcaption></figure>')
    book = '<path class="card" d="M8 14 Q20 8 32 14 V50 Q20 44 8 50 Z"/><path class="card" d="M56 14 Q44 8 32 14 V50 Q44 44 56 50 Z"/>'
    cal = ('<rect class="card" x="8" y="12" width="48" height="44" rx="6"/><path class="st" d="M8 26 H56 M20 6 V16 M44 6 V16"/>'
           '<text class="ts" x="32" y="46" text-anchor="middle">Thu 7</text>')
    ask = ('<path class="card" d="M10 12 H54 a6 6 0 0 1 6 6 V38 a6 6 0 0 1 -6 6 H32 L20 56 V44 H10 a6 6 0 0 1 -6 -6 V18 a6 6 0 0 1 6 -6 Z" transform="translate(0 -2)"/>'
           '<text class="ts big2" x="32" y="36" text-anchor="middle">?</text>')
    todo = ''
    for i, y in enumerate((18, 32, 46)):
        todo += f'<rect class="card" x="8" y="{y - 6}" width="12" height="12" rx="2"/><path class="stm" d="M28 {y} H56"/>'
        if i < 2:
            todo += f'<path class="shi" d="M10.5 {y} l3 3 l5 -7"/>'
    fix = '<path class="st" d="M12 52 L38 26" stroke-width="5"/><path class="card" d="M30 12 L52 34 L44 42 L22 20 Z"/>'
    return ('<div class="icons">' + wrap(book, 'Learning') + wrap(cal, 'Organizing') + wrap(ask, 'Asking')
            + wrap(todo, 'Finishing') + wrap(fix, 'Fixing') + '</div>')


# ------------------------------------------------------------------ BE
def fig_shelf():
    u = 'sh'
    b = [T(10, 52, 'Everything you could try', 'mono b')]
    labels = ['unusual', 'embarrassing', 'kind of crazy', '...', '...', '...']
    for i, lab in enumerate(labels):
        x = 10 + i * 96
        b.append(f'<rect class="dimbox" x="{x}" y="80" width="92" height="90" rx="6"/>')
        b.append(T(x + 46, 130, lab, 'small', 'middle'))
    x = 10 + 6 * 96
    b.append(f'<rect class="hibox" x="{x}" y="80" width="92" height="90" rx="6"/>')
    b.append(T(x + 46, 120, 'the default', 'small b', 'middle'))
    b.append(T(x + 46, 138, 'answer', 'small b', 'middle'))
    b.append('<path class="stm" d="M5 176 H680"/>')
    b.append('<path class="stm" d="M10 196 V204 H582 V196"/>')
    b.append(T(296, 224, 'ruled out before you noticed you were deciding', 'small', 'middle'))
    b.append(T(x + 46, 204, 'what you do', 'small', 'middle'))
    return svg('0 0 690 240', 'A shelf of solutions where most are never looked at and only the default answer is taken', ''.join(b), u)


def fig_attention():
    u = 'at'
    b = []
    # left: braced
    b.append('<rect class="room" x="20" y="130" width="300" height="140" rx="8"/>')
    b.append(person(170, 172, 1.0, 'st', legs=True))
    for (bx, by, lab) in ((70, 46, 'replaying'), (170, 30, 'how do I look?'), (270, 46, 'rehearsing')):
        w = 8 * len(lab) + 22
        b.append(f'<rect class="bubble" x="{bx - w / 2:.0f}" y="{by - 16}" width="{w:.0f}" height="30" rx="15"/>')
        b.append(T(bx, by + 4, lab, 'small', 'middle'))
        b.append(f'<path class="stm dash" d="M{bx} {by + 14} L{170 + (bx - 170) * 0.15:.0f} 158"/>')
    b.append(T(170, 322, 'Braced: body here, attention elsewhere', 't', 'middle'))
    # right: here
    b.append('<rect class="room" x="360" y="130" width="300" height="140" rx="8"/>')
    b.append(person(400, 172, 1.0, 'st', legs=True))
    b.append(person(590, 190, 0.8, 'stm', legs=True))
    b.append('<rect class="card" x="470" y="238" width="50" height="26" rx="3"/>')
    b.append(f'<path class="hi" d="M413 168 L576 178" marker-end="url(#a{u}hi)"/>')
    b.append(f'<path class="hi" d="M412 204 L466 240" marker-end="url(#a{u}hi)"/>')
    b.append('<circle class="fhi" cx="400" cy="206" r="5"/>')
    b.append('<path class="stm dash" d="M380 126 L397 198"/>')
    b.append(T(372, 112, 'the feeling in you right now', 'small'))
    b.append(T(495, 288, 'the task', 'small', 'middle'))
    b.append(T(495, 302, 'in your hands', 'small', 'middle'))
    b.append(T(610, 288, 'the person', 'small', 'middle'))
    b.append(T(610, 302, 'in front of you', 'small', 'middle'))
    b.append(T(510, 322, 'Here: attention on what is going on', 't', 'middle'))
    return svg('0 0 680 336', 'Two rooms: a braced person whose attention is in the past and the future, and a present person whose attention is on the person, task and feeling in front of them', ''.join(b), u)


def fig_legs():
    u = 'lg'
    gy = 220
    b = [f'<path class="stm" d="M20 {gy} H640"/>']

    def fig(x, mode):
        o = [f'<circle class="st" cx="{x}" cy="70" r="14"/>',
             f'<path class="st" d="M{x} 84 V140 M{x} 100 L{x - 28} 124 M{x} 100 L{x + 28} 124"/>']
        if mode == 'do':
            o.append(f'<path class="sdo" d="M{x} 140 L{x + 6} {gy}"/>')
            o.append(f'<path class="sbe" d="M{x} 140 L{x - 30} 160 L{x - 46} 148"/>')
        elif mode == 'be':
            o.append(f'<path class="sbe" d="M{x} 140 L{x - 6} {gy}"/>')
            o.append(f'<path class="sdo" d="M{x} 140 L{x + 30} 160 L{x + 46} 148"/>')
        else:
            o.append(f'<path class="sdo" d="M{x} 140 L{x + 30} {gy}"/>')
            o.append(f'<path class="sbe" d="M{x} 140 L{x - 30} {gy}"/>')
            o.append(f'<path class="stm" d="M{x - 52} {gy + 10} q8 -8 16 0 M{x + 36} {gy + 10} q8 -8 16 0"/>')
        return ''.join(o)

    b.append(fig(110, 'do'))
    b.append(fig(330, 'be'))
    b.append(fig(550, 'walk'))
    for x, l1, l2 in ((110, 'Driven', 'hops on the DO leg'), (330, 'Drifting', 'hops on the BE leg'), (550, 'High agency', 'both legs, wobbly at first')):
        b.append(T(x, 250, l1, 'small b', 'middle'))
        b.append(T(x, 266, l2, 'small', 'middle'))
    b.append('<path class="sdo" d="M30 24 H60"/>' + T(68, 28, 'DO leg', 'small') + '<path class="sbe" d="M140 24 H170"/>' + T(178, 28, 'BE leg', 'small'))
    return svg('0 0 660 280', 'Three stick figures: one hopping on the DO leg, one hopping on the BE leg, one walking on both', ''.join(b), u)


def fig_loop():
    u = 'lp'
    b = []

    def node(cx, cy, l1, l2):
        return (f'<rect class="card" x="{cx - 88}" y="{cy - 29}" width="176" height="58" rx="10"/>'
                + T(cx, cy - 4, l1, 'small b', 'middle') + T(cx, cy + 14, l2, 'small', 'middle'))

    b.append(node(280, 50, 'BE widens', 'what you can see'))
    b.append(node(470, 190, 'DO tests', 'the fears'))
    b.append(node(280, 330, 'fears turn out smaller', 'than they looked'))
    b.append(node(90, 190, 'tension loosens', 'a little more'))
    b.append(arrow(u, 'M368 50 C440 50 470 100 470 158', 'hi', 'stg'))
    b.append(arrow(u, 'M470 222 C470 280 440 330 368 330', 'hi', 'stg'))
    b.append(arrow(u, 'M192 330 C120 330 90 280 90 222', 'hi', 'stg'))
    b.append(arrow(u, 'M90 158 C90 100 120 50 192 50', 'hi', 'stg'))
    b.append(T(280, 186, 'BE and DO', 't', 'middle'))
    b.append(T(280, 206, 'in a loop', 'small', 'middle'))
    return svg('0 0 560 380', 'A loop: being here widens what you see, doing tests your fears, fears turn out smaller, tension loosens, and you see more', ''.join(b), u)


def fig_jail():
    u = 'jl'
    b = ['<rect class="room" x="20" y="20" width="200" height="200" rx="6"/>']
    for i in range(7):
        x = 45 + i * 25
        b.append(f'<path class="st" d="M{x} 20 V220"/>')
    b.append(person(120, 104, 0.9, 'stm', legs=True))
    b.append('<rect class="card" x="290" y="24" width="104" height="196" rx="14"/>')
    for i in range(5):
        y = 56 + i * 32
        b.append(f'<circle class="{"fhi" if i == 2 else "fmu"}" cx="314" cy="{y}" r="9"/>')
        b.append(f'<path class="{"shi" if i == 2 else "stm"}" d="M332 {y} H376"/>')
    b.append(f'<path class="shi" d="M308 {56 + 64} l5 5 l9 -11"/>')
    b.append(T(420, 112, 'Who do', 'big3'))
    b.append(T(420, 146, 'you call?', 'big3'))
    return svg('0 0 560 240', 'A person behind bars and a phone with a short contact list: who do you call?', ''.join(b), u)


# ------------------------------------------------------------------ math
def fig_bars():
    u = 'br'
    x0 = 150
    sc = 2.1
    b = []
    for i, (lab, v, cls) in enumerate((('100 DO \u00d7 1 BE', 100, 'fdo'), ('95 DO \u00d7 2 BE', 190, 'fhi'))):
        y = 30 + i * 70
        b.append(T(x0 - 12, y + 24, lab, 'mono b', 'end'))
        b.append(f'<rect class="{cls} bar" x="{x0}" y="{y}" width="{v * sc:.0f}" height="38" rx="3"/>')
        b.append(T(x0 + v * sc + 10, y + 25, f'= {v}', 't'))
    b.append(T(x0, 182, 'Five points less DO for one point more BE: almost twice as effective.', 'small'))
    return svg('0 0 640 200', 'Two bars: 100 times 1 equals 100, 95 times 2 equals 190', ''.join(b), u)


def fig_anokhin():
    u = 'an'
    b = []

    def box(x, y, w, h, l1, l2='', cls='card'):
        s = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/>'
        if l2:
            s += T(x + w / 2, y + h / 2 - 3, l1, 'small b', 'middle') + T(x + w / 2, y + h / 2 + 14, l2, 'small', 'middle')
        else:
            s += T(x + w / 2, y + h / 2 + 4, l1, 'small b', 'middle')
        return s

    b.append(box(20, 15, 200, 50, 'Need, situation,', 'memory'))
    b.append(box(20, 95, 200, 50, 'Decision'))
    b.append(box(20, 175, 200, 50, 'Action'))
    b.append(box(20, 255, 200, 50, 'Result'))
    b.append(box(330, 85, 290, 66, 'Acceptor: a model of', 'the result you aim at', 'cardhi'))
    b.append(box(330, 205, 290, 50, 'Compare what happened', 'with the model'))
    b.append(box(330, 285, 135, 46, 'match:', 'next step'))
    b.append(box(485, 285, 135, 46, 'mismatch:', 'search again'))
    b.append(arrow(u, 'M120 65 V95', 'ink'))
    b.append(arrow(u, 'M120 145 V175', 'ink'))
    b.append(arrow(u, 'M120 225 V255', 'ink'))
    b.append(arrow(u, 'M220 120 H330', 'hi', 'stg'))
    b.append(arrow(u, 'M220 280 C280 280 290 240 330 232', 'ink'))
    b.append(arrow(u, 'M475 151 V205', 'hi', 'stg'))
    b.append(arrow(u, 'M400 255 V285', 'ink'))
    b.append(arrow(u, 'M550 255 V285', 'ink'))
    return svg('0 0 650 345', 'Anokhin loop, simplified: need and memory lead to a decision, a model of the aimed result forms, action produces a result, and the result is compared with the model', ''.join(b), u)


def fig_studies():
    u = 'sd'
    base = 215
    k = 0.5
    b = []

    def bar(x, v, cls, lab):
        h = v * k
        return (f'<rect class="{cls} bar" x="{x}" y="{base - h:.0f}" width="54" height="{h:.0f}" rx="3"/>'
                + T(x + 27, base - h - 8, str(v), 't', 'middle') + T(x + 27, base + 18, lab, 'small', 'middle'))

    b.append('<path class="stm" d="M20 215 H620"/>')
    b.append(bar(40, 100, 'fmu', 'before') + bar(104, 242, 'fhi', 'after') + T(97, 40, 'Time on the phone', 'small b', 'middle'))
    b.append(bar(190, 100, 'fmu', 'before') + bar(254, 271, 'fhi', 'after') + T(247, 40, 'Money raised', 'small b', 'middle'))
    b.append(T(147, 252, 'Callers who spent five minutes with', 'small', 'middle'))
    b.append(T(147, 268, 'the student, one month on (Grant, 2007)', 'small', 'middle'))
    b.append(T(147, 284, 'Readers of his letter and callers who', 'small', 'middle'))
    b.append(T(147, 300, 'never met him: no significant gains', 'small', 'middle'))
    b.append(bar(430, 100, 'fmu', 'lower') + bar(494, 83, 'fhi', 'higher') + T(487, 40, 'Risk of dying during follow-up', 'small b', 'middle'))
    b.append(T(487, 252, 'Lower or higher sense of purpose', 'small', 'middle'))
    b.append(T(487, 268, '(Cohen and colleagues, 2016)', 'small', 'middle'))
    b.append(T(487, 284, 'adjusted relative risk 0.83', 'small', 'middle'))
    b.append(T(487, 300, '(95% CI 0.75 to 0.91)', 'small', 'middle'))
    b.append(T(147, 330, 'Index: their own level before = 100', 'small', 'middle'))
    b.append(T(487, 330, 'Index: lower purpose = 100', 'small', 'middle'))
    return svg('0 0 640 345', 'Left: callers who spent five minutes with a scholarship student went from 100 to 242 in phone time and from 100 to 271 in money raised a month later. Right: people with a higher sense of purpose had a relative risk of dying of 83 against 100', ''.join(b), u)

def scale(cx, tilt, left, right, title, uid):
    ang = math.radians(tilt)
    half = 130
    top = 120
    lx, ly = cx - half * math.cos(ang), top - half * math.sin(ang)
    rx, ry = cx + half * math.cos(ang), top + half * math.sin(ang)
    o = [f'<path class="st" d="M{cx} {top} V236"/>', f'<path class="card" d="M{cx - 40} 258 L{cx} 230 L{cx + 40} 258 Z"/>',
         f'<path class="st" d="M{lx:.0f} {ly:.0f} L{rx:.0f} {ry:.0f}" stroke-width="4"/>']
    for (px, py, (lab, w, cls)) in ((lx, ly, left), (rx, ry, right)):
        o.append(f'<path class="stm" d="M{px:.0f} {py:.0f} L{px - 40:.0f} {py + 56:.0f} M{px:.0f} {py:.0f} L{px + 40:.0f} {py + 56:.0f}"/>')
        o.append(f'<path class="stm" d="M{px - 44:.0f} {py + 56:.0f} H{px + 44:.0f}" stroke-width="3"/>')
        o.append(f'<rect class="{cls}" x="{px - w / 2:.0f}" y="{py + 56 - w * 0.7:.0f}" width="{w}" height="{w * 0.7:.0f}" rx="4"/>')
        lines = lab.split('|')
        for j, ln in enumerate(lines):
            o.append(T(px, py - 14 - (len(lines) - 1 - j) * 16, ln, 'small', 'middle'))
    o.append(T(cx, 300, title, 't', 'middle'))
    return ''.join(o)


def fig_scales():
    u = 'sc'
    b = scale(200, 9, ('the fear', 58, 'fdo'), ('a bit more peace', 24, 'fmu'), 'Usually: the fear wins', u)
    b += scale(600, -9, ('the fear, still there', 40, 'fdo'), ('a reason|bigger than me', 66, 'fhi'), 'With a bigger reason: outvoted', u)
    return svg('0 0 800 320', 'Two balance scales: usually fear outweighs a bit more peace; with a reason bigger than you, the reason outweighs the fear', b, u)


def fig_spot():
    u = 'sp'
    b = ['<polygon class="cone" points="320,8 240,236 400,236"/>']
    b.append(person(320, 150, 1.0, 'st', legs=True))
    b.append(T(320, 270, 'you, sure that everyone is watching', 't', 'middle'))
    heads = [(60, 'lunch?'), (140, 'my email'), (500, 'my hair'), (580, 'am I late?')]
    for x, lab in heads:
        b.append(f'<circle class="stm" cx="{x}" cy="196" r="13"/>')
        b.append(f'<path class="stm" d="M{x} 209 V236"/>')
        w = 8 * len(lab) + 18
        b.append(f'<rect class="bubble" x="{x - w / 2:.0f}" y="132" width="{w}" height="28" rx="14"/>')
        b.append(T(x, 150, lab, 'small', 'middle'))
        b.append(f'<path class="stm dash" d="M{x} 160 V183"/>')
    return svg('0 0 640 290', 'A person in a spotlight while the people around them think about lunch, email and their own hair', ''.join(b), u)


def fig_finish():
    u = 'fn'
    b = [T(20, 24, 'A goal about you', 't')]
    b.append('<path class="st" d="M30 100 H330"/>')
    b.append(person(110, 56, 0.5, 'st', legs=True))
    b.append('<path class="st" d="M330 60 V100"/><path class="fdo" d="M330 60 L356 69 L330 78 Z"/>')
    for x in (400, 470):
        b.append(f'<path class="stm dash" d="M{x} 60 V100"/><path class="fmu2 ghost" d="M{x} 60 L{x + 26} 69 L{x} 78 Z"/>')
    b.append('<path class="stm dash" d="M330 100 H500"/>')
    b.append(T(560, 82, 'the finish line', 'small', 'middle'))
    b.append(T(560, 98, 'steps back', 'small', 'middle'))
    b.append(T(20, 134, 'A reason about someone else', 't'))
    b.append('<path class="stg" d="M30 210 H600" marker-end="url(#afnhi)"/>')
    b.append(person(110, 166, 0.5, 'st', legs=True))
    b.append(T(315, 236, 'no finish line', 'small', 'middle'))
    return svg('0 0 640 250', 'A goal has a finish line that steps back when you arrive; a reason about someone else is a road with no finish line', ''.join(b), u)


def fig_pushpull():
    u = 'pp'
    x0, x1, y0, y1 = 70, 570, 20, 400
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    b = [f'<rect class="q default" x="{x0}" y="{my}" width="{mx - x0}" height="{y1 - my}"/>',
         f'<rect class="q driven" x="{mx}" y="{my}" width="{x1 - mx}" height="{y1 - my}"/>',
         f'<rect class="q drifting" x="{x0}" y="{y0}" width="{mx - x0}" height="{my - y0}"/>',
         f'<rect class="q high" x="{mx}" y="{y0}" width="{x1 - mx}" height="{my - y0}"/>',
         f'<circle class="ringm" cx="{mx}" cy="{my}" r="40"/>']
    pushes = [((130, 70), (mx - 34, my - 26)), ((110, 150), (mx - 40, my - 8)),
              ((500, 360), (mx + 34, my + 26)), ((540, 290), (mx + 40, my + 10))]
    for (sx, sy), (ex, ey) in pushes:
        b.append(arrow(u, f'M{sx} {sy} L{ex:.0f} {ey:.0f}', 'mu', 'stm2'))
    b.append(T(136, 62, 'the money runs out', 'small'))
    b.append(T(116, 142, 'the plateau', 'small'))
    b.append(T(506, 380, 'a crash', 'small'))
    b.append(T(566, 272, 'burnout', 'small', 'end'))
    b.append(arrow(u, f'M{mx + 30} {my - 28} L{x1 - 30} {y0 + 30}', 'hi', 'climb'))
    b.append(T(x1 - 12, 178, 'a pull:', 't', 'end'))
    b.append(T(x1 - 12, 196, 'a reason bigger than you', 'small b', 'end'))
    b.append(T(mx, y1 + 30, 'pushes bring you to the middle; a pull takes you across', 'small', 'middle'))
    return svg('0 0 640 440', 'Pushes from both sides bring a person to the middle; a pull from a reason bigger than themselves takes them across', ''.join(b), u)


def fig_tv():
    u = 'tv'
    b = ['<rect class="card" x="330" y="30" width="250" height="160" rx="10"/>']
    b.append('<rect class="screen" x="342" y="42" width="226" height="136" rx="4"/>')
    b.append(person(455, 70, 0.8, 'st', legs=True))
    b.append(T(455, 164, 'your life', 'small', 'middle'))
    b.append('<path class="st" d="M420 190 V206 M490 190 V206 M400 206 H510"/>')
    b.append('<rect class="card" x="30" y="170" width="190" height="60" rx="10"/>')
    b.append('<rect class="cardm" x="22" y="140" width="28" height="90" rx="10"/><rect class="cardm" x="200" y="140" width="28" height="90" rx="10"/>')
    b.append(person(120, 112, 0.9, 'st', legs=False))
    b.append('<path class="stm dash" d="M138 108 L326 100"/>')
    b.append(T(300, 252, 'awareness without being in it', 't', 'middle'))
    return svg('0 0 620 270', 'A person on a sofa watching a screen that shows their own life', ''.join(b), u)


# ------------------------------------------------------------------ more
def icons_flow_html():
    def wrap(inner, label, sub):
        return (f'<figure class="ic"><svg class="chart icon" viewBox="0 0 64 64" role="img" aria-label="{label}">{inner}</svg>'
                f'<figcaption>{label}<br><span>{sub}</span></figcaption></figure>')
    code = ('<rect class="card" x="8" y="14" width="48" height="30" rx="3"/><path class="st" d="M4 50 H60"/>'
            '<text class="ts" x="32" y="34" text-anchor="middle">&lt;/&gt;</text>')
    ball = ('<circle class="card" cx="32" cy="32" r="22"/>'
            '<path class="st" d="M10 32 H54 M32 10 V54 M17 16 Q32 32 17 48 M47 16 Q32 32 47 48"/>')
    note = ('<path class="st" d="M24 46 V16 L48 10 V40"/><ellipse class="card" cx="19" cy="47" rx="8" ry="6"/>'
            '<ellipse class="card" cx="43" cy="41" rx="8" ry="6"/>')
    sun = '<circle class="sunf" cx="32" cy="32" r="11"/>'
    for k in range(8):
        a = math.radians(k * 45)
        sun += f'<path class="st" d="M{32 + 16 * math.cos(a):.1f} {32 + 16 * math.sin(a):.1f} L{32 + 24 * math.cos(a):.1f} {32 + 24 * math.sin(a):.1f}"/>'
    heart = '<path class="heartf" d="M32 56 C8 40 6 22 19 15 C26 12 32 17 32 22 C32 17 38 12 45 15 C58 22 56 40 32 56 Z"/>'
    return ('<div class="icons">' + wrap(code, 'Programmers', 'flow') + wrap(ball, 'Athletes', 'the zone') + wrap(note, 'Musicians', 'the muse')
            + wrap(sun, 'The rest of us', 'a good day') + wrap(heart, 'Everyone', 'being in love') + '</div>')


def fig_footsteps():
    u = 'ft'
    x0, y0, x1, y1 = 70, 330, 580, 40
    ang = math.atan2(y1 - y0, x1 - x0)
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    b = [f'<path class="diag" d="M{x0} {y0} L{x1} {y1}"/>']
    n = 12
    for k in range(n):
        t = (k + 0.6) / n
        cx = x0 + (x1 - x0) * t
        cy = y0 + (y1 - y0) * t
        side = 1 if k % 2 == 0 else -1
        px, py = cx + nx * 15 * side, cy + ny * 15 * side
        cls = 'fdo' if side == 1 else 'fbe'
        deg = math.degrees(ang)
        b.append(f'<ellipse class="{cls} foot" cx="{px:.1f}" cy="{py:.1f}" rx="17" ry="8" transform="rotate({deg:.1f} {px:.1f} {py:.1f})"/>')
    b.append(T(x0, y0 + 34, 'DO, BE, DO, BE', 't'))
    b.append(T(x1, y1 - 16, 'in step', 't', 'end'))
    b.append('<path class="sdo" d="M360 330 H390"/>' + T(398, 334, 'DO foot', 'small') + '<path class="sbe" d="M480 330 H510"/>' + T(518, 334, 'BE foot', 'small'))
    return svg('0 0 640 380', 'Footprints alternating between a DO foot and a BE foot along the line of harmony, walking in step', ''.join(b), u)


def fig_inertia():
    u = 'in'
    x0, x1, y0, y1 = 70, 570, 20, 400
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    b = [f'<rect class="q default" x="{x0}" y="{my}" width="{mx - x0}" height="{y1 - my}"/>',
         f'<rect class="q driven" x="{mx}" y="{my}" width="{x1 - mx}" height="{y1 - my}"/>',
         f'<rect class="q drifting" x="{x0}" y="{y0}" width="{mx - x0}" height="{my - y0}"/>',
         f'<rect class="q high" x="{mx}" y="{y0}" width="{x1 - mx}" height="{my - y0}"/>',
         f'<circle class="ringm" cx="{mx}" cy="{my}" r="40"/>']
    sx, sy = 520, 360
    b.append(f'<circle class="dot ink" cx="{sx}" cy="{sy}" r="6"/>')
    b.append(f'<path class="stm dash" d="M{sx} {sy} L548 52"/>')
    b.append('<path class="st" d="M526 200 L546 220 M546 200 L526 220"/>')
    b.append(T(508, 214, "can't aim straight", 'small', 'end'))
    b.append(T(508, 230, 'from out here', 'small', 'end'))
    b.append(arrow(u, f'M{sx} {sy} C440 340 340 300 {mx} {my + 10} S470 120 546 56', 'hi', 'climb'))
    b.append(T(sx - 4, sy + 30, 'years of momentum', 'small', 'end'))
    b.append(T(mx - 56, my + 70, 'back through the middle,', 'small b', 'end'))
    b.append(T(mx - 56, my + 86, 'then climb', 'small b', 'end'))
    b.append(T(mx, y1 + 30, 'inertia: the route to the corner goes through the middle', 'small', 'middle'))
    return svg('0 0 640 440', 'From deep in the Driven room you cannot aim straight at the corner; the route goes back through the middle and then climbs', ''.join(b), u)


# ------------------------------------------------------------------ driven, drifting, top right
def fig_week():
    u = 'wk'
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    b = []
    for i, d in enumerate(days):
        x = 51 + i * 78
        work = i < 5
        b.append(T(x + 35, 48, d, 'small', 'middle'))
        b.append(f'<rect class="fdo{"" if work else " fsoft"}" x="{x}" y="60" width="70" height="104" rx="8"/>')
        b.append(f'<text class="wt" x="{x + 35}" y="118" text-anchor="middle">{"work" if work else "study"}</text>')
    b.append(T(320, 194, 'the background hum, all week:', 'small b', 'middle'))
    b.append(T(320, 212, 'not good enough \u00b7 not good enough \u00b7 not good enough \u00b7 not good enough', 'small faint', 'middle'))
    return svg('0 0 640 232', 'A week with five days of work and two days of study, and the thought not good enough humming underneath', ''.join(b), u)


def fig_wall():
    u = 'wl'
    b = ['<path class="stm" d="M20 210 H620"/>']
    # person leaning into a wall
    b.append('<circle class="st" cx="150" cy="94" r="12"/>')
    b.append('<path class="st" d="M146 106 L112 160 M146 114 L228 122 M146 122 L226 140 M112 160 L94 210 M112 160 L132 210"/>')
    b.append('<rect class="wallr" x="236" y="50" width="30" height="160" rx="3"/>')
    b.append(arrow(u, 'M96 66 L212 66', 'do', 'sdo2'))
    b.append(T(150, 52, 'more force', 'small b', 'middle'))
    # the door nobody tries
    b.append('<rect class="room" x="420" y="90" width="76" height="120" rx="3"/>')
    b.append('<path class="card" d="M420 90 L392 102 L392 202 L420 210 Z"/>')
    b.append('<circle class="fhi" cx="404" cy="156" r="3"/>')
    b.append(T(458, 236, 'the door next to it', 'small', 'middle'))
    b.append(T(250, 236, 'the only direction you can see', 'small', 'middle'))
    return svg('0 0 640 250', 'A person pushing harder and harder against a wall while an open door stands unnoticed beside it', ''.join(b), u)


def fig_hammock():
    u = 'hm'
    b = ['<path class="stm" d="M20 235 H620"/>', '<circle class="sunf" cx="548" cy="58" r="26"/>']
    b.append('<path class="trunk" d="M150 235 C160 180 170 130 190 90"/>')
    for d in ('M190 90 C160 70 130 80 108 102', 'M190 90 C170 60 150 50 118 52', 'M190 90 C200 60 230 50 262 60',
              'M190 90 C222 84 252 96 272 120', 'M190 90 C184 66 190 46 206 30'):
        b.append(f'<path class="frond" d="{d}"/>')
    b.append('<path class="trunk" d="M470 235 V122"/>')
    b.append('<path class="card" d="M192 128 Q330 224 470 124 Q330 196 192 128 Z"/>')
    b.append('<circle class="st" cx="286" cy="176" r="11"/>')
    b.append('<path class="st" d="M297 182 Q340 202 388 180 M388 180 L412 160 L430 150"/>')
    b.append('<path class="st" d="M322 192 L332 176"/>')
    b.append(T(300, 142, 'z z z', 'small'))
    b.append(T(548, 112, 'no winter to survive', 'small', 'middle'))
    b.append(T(310, 258, 'no deadline, nobody waiting on an answer', 'small', 'middle'))
    return svg('0 0 640 270', 'A hammock between a palm tree and a post, with a person asleep and the sun out: nothing pushing from the outside', ''.join(b), u)


def fig_gym():
    u = 'gy'
    b = ['<path class="stm" d="M20 222 H620"/>']
    b.append('<rect class="card" x="40" y="132" width="250" height="10" rx="2"/><path class="st" d="M60 142 V222 M270 142 V222"/>')
    for i in range(5):
        x = 62 + i * 46
        b.append(f'<rect class="card" x="{x}" y="104" width="9" height="28" rx="2"/><rect class="card" x="{x + 27}" y="104" width="9" height="28" rx="2"/>'
                 f'<path class="st" d="M{x + 9} 118 H{x + 27}"/>')
    b.append(T(165, 66, 'such weights', 'dg2 c3', 'middle'))
    b.append(T(165, 90, 'very untouched', 'dg2 c2', 'middle'))
    b.append('<rect class="card" x="350" y="188" width="110" height="12" rx="2"/><path class="st" d="M364 200 V222 M446 200 V222"/>')
    b.append('<circle class="st" cx="385" cy="148" r="11"/><path class="st" d="M385 159 V188 M385 188 L418 188 M418 188 V220 M385 170 L406 178"/>')
    b.append('<circle class="st" cx="540" cy="150" r="10"/><path class="st" d="M540 160 V196 M540 170 L520 186 M540 170 L560 180 M540 196 L528 222 M540 196 L552 222"/>')
    for (bx, by, lab, col) in ((402, 96, 'much calm', 'c1'), (548, 96, 'so peaceful', 'c3')):
        w = 10 * len(lab) + 24
        b.append(f'<rect class="bubble" x="{bx - w / 2:.0f}" y="{by - 15}" width="{w}" height="30" rx="15"/>' + T(bx, by + 5, lab, f'dg2 {col}', 'middle'))
        b.append(f'<path class="stm dash" d="M{bx} {by + 15} V130"/>')
    b.append('<rect class="card" x="470" y="20" width="110" height="38" rx="4"/>')
    b.append(T(525, 47, 'wow', 'dg2 big4 c2', 'middle'))
    return svg('0 0 640 245', 'A gym where nobody lifts, in doge style: such weights, very untouched, much calm, so peaceful, wow', ''.join(b), u)

def fig_inout():
    u = 'io'
    b = []
    # inside: a fan of options
    b.append(person(170, 214, 0.9, 'st', legs=True))
    for k in range(9):
        ang = math.radians(-160 + k * 17.5)
        x2 = 170 + 118 * math.cos(ang)
        y2 = 198 + 118 * math.sin(ang)
        b.append(arrow(u, f'M170 198 L{x2:.0f} {y2:.0f}', 'hi', 'hi'))
    b.append(T(170, 326, 'Inside: more options', 't', 'middle'))
    # outside: steady, others lean in
    b.append(person(500, 214, 0.9, 'st', legs=True))
    for x in (400, 598):
        b.append(person(x, 240, 0.6, 'stm', legs=True))
        d = 'M{} 236 L{} 236'.format(x + (16 if x < 500 else -16), 500 + (-26 if x < 500 else 26))
        b.append(arrow(u, d, 'hi', 'hi'))
    b.append('<rect class="card" x="480" y="40" width="40" height="64" rx="8"/>')
    b.append('<path class="stm" d="M470 56 q-8 14 0 28 M530 56 q8 14 0 28 M462 50 q-14 20 0 40 M538 50 q14 20 0 40"/>')
    b.append(T(500, 24, 'the phone rings', 'small', 'middle'))
    b.append(T(500, 326, 'Outside: people find you steady', 't', 'middle'))
    return svg('0 0 680 340', 'Inside, a fan of options opens up; outside, other people lean toward someone steady and the phone rings', ''.join(b), u)


def knob(cx, cy, angle_deg, lab_l, lab_r):
    """A volume knob. angle_deg: 0 = pointing left (zero), 180 = pointing right (full)."""
    a = math.radians(180 + angle_deg)
    x2, y2 = cx + 15 * math.cos(a), cy + 15 * math.sin(a)
    o = [f'<circle class="card" cx="{cx}" cy="{cy}" r="22"/>',
         f'<path class="st" d="M{cx} {cy} L{x2:.1f} {y2:.1f}"/>',
         T(cx - 34, cy + 22, lab_l, 'small', 'end'), T(cx + 34, cy + 22, lab_r, 'small')]
    return ''.join(o)


def fig_stoic():
    u = 'sto'
    b = [T(170, 26, 'The internet version', 't', 'middle'), T(505, 26, "Marcus's notebook", 't', 'middle')]
    # left: a rock with the volume at zero
    b.append('<path class="rockf" d="M100 196 C88 140 124 94 170 94 C218 94 252 140 240 196 Z"/>')
    b.append('<path class="st" d="M144 138 H158 M184 138 H198 M152 164 H190"/>')
    b.append(T(170, 78, 'be a rock', 'small b', 'middle'))
    b.append(knob(170, 244, 0, '0', '10'))
    b.append(T(170, 292, 'feelings: off', 'small', 'middle'))
    # right: an open notebook
    b.append('<rect class="card" x="372" y="66" width="130" height="146" rx="4"/><rect class="card" x="502" y="66" width="130" height="146" rx="4"/>')
    for y in (96, 114, 132):
        b.append(f'<path class="stm" d="M386 {y} H488"/>')
    b.append(T(516, 94, 'note to self:', 'small b'))
    b.append(T(516, 114, "don't snap at", 'small'))
    b.append(T(516, 130, 'difficult people', 'small'))
    b.append(T(516, 152, '(talk it over)', 'small'))
    b.append('<path class="heartf" transform="translate(588 168) scale(.5)" d="M32 56 C8 40 6 22 19 15 C26 12 32 17 32 22 C32 17 38 12 45 15 C58 22 56 40 32 56 Z"/>')
    b.append(knob(505, 244, 100, '0', '10'))
    b.append(T(505, 292, 'feelings: on, and worked on', 'small', 'middle'))
    return svg('0 0 680 306', 'Left, a rock with its feelings volume at zero; right, an open notebook where Marcus tells himself not to snap at difficult people, with the volume on', ''.join(b), u)


def fig_stops():
    u = 'st'

    def icon(kind):
        if kind == 'battery':
            return ('<rect class="card" x="6" y="20" width="44" height="26" rx="4"/><rect class="card" x="50" y="28" width="6" height="10" rx="1"/>'
                    '<rect class="fdo" x="10" y="24" width="9" height="18" rx="2"/><path class="stm dash" d="M24 33 H44"/>')
        if kind == 'trophy':
            return ('<path class="card" d="M20 12 H44 V28 Q44 40 32 42 Q20 40 20 28 Z"/><path class="st" d="M20 16 H12 Q12 28 22 30 M44 16 H52 Q52 28 42 30 M32 42 V52 M22 54 H42"/>'
                    '<ellipse class="fmu" cx="50" cy="10" rx="9" ry="5" style="fill-opacity:.55"/>')
        if kind == 'plaster':
            return ('<g transform="rotate(-35 32 32)"><rect class="card" x="6" y="22" width="52" height="20" rx="9"/><rect class="cardm" x="23" y="22" width="18" height="20"/>'
                    '<circle class="fmu" cx="29" cy="28" r="1.4"/><circle class="fmu" cx="35" cy="28" r="1.4"/><circle class="fmu" cx="29" cy="36" r="1.4"/><circle class="fmu" cx="35" cy="36" r="1.4"/></g>')
        if kind == 'heart':
            return ('<path class="heartf" d="M32 56 C8 40 6 22 19 15 C26 12 32 17 32 22 C32 17 38 12 45 15 C58 22 56 40 32 56 Z"/>'
                    '<path class="st" d="M34 18 L28 30 L37 36 L30 50"/>')
        if kind == 'wallet':
            return ('<rect class="card" x="6" y="16" width="52" height="36" rx="6"/><path class="st" d="M6 26 H58"/><circle class="card" cx="48" cy="40" r="4"/>'
                    '<text class="ts big2" x="26" y="48" text-anchor="middle">0</text>')
        if kind == 'house':
            return ('<path class="card" d="M6 32 L32 10 L58 32 V54 H6 Z"/><text class="ts big2" x="32" y="47" text-anchor="middle" style="fill:var(--drifting)">!</text>')
        if kind == 'plateau':
            return ('<path class="stm" d="M8 54 H58 M8 54 V8"/><path class="shi" d="M10 50 L26 32 L38 22 H58"/>')
        return ''

    def card(x, kind, lines, accent):
        o = f'<rect class="room" x="{x}" y="46" width="84" height="88" rx="10"/>'
        o += f'<g transform="translate({x + 10} {54})">{icon(kind)}</g>'
        for j, ln in enumerate(lines):
            o += T(x + 42, 152 + j * 14, ln, 'small', 'middle')
        return o

    b = [T(200, 26, 'Driven: usually a crash', 't', 'middle'), T(554, 26, 'Drifting: three things', 't', 'middle')]
    left = [('battery', ['burnout']), ('trophy', ['the goal', 'reached,', 'then empty']), ('plaster', ['a body that', 'stops', 'cooperating']), ('heart', ['someone', 'close is', 'hurt'])]
    for i, (k, ln) in enumerate(left):
        b.append(card(20 + i * 92, k, ln, 'do'))
    right = [('wallet', ['the money', 'runs out']), ('house', ['something', 'happens at', 'home']), ('plateau', ['the plateau'])]
    for i, (k, ln) in enumerate(right):
        b.append(card(420 + i * 92, k, ln, 'be'))
    b.append(arrow(u, 'M200 200 L322 280', 'ink', 'st'))
    b.append(arrow(u, 'M554 200 L378 280', 'ink', 'st'))
    b.append('<circle class="ringm" cx="350" cy="300" r="26"/>')
    b.append(T(350, 350, 'the middle', 't', 'middle'))
    return svg('0 0 700 364', 'What stops a driven person: burnout, the goal reached and then empty, a body that stops cooperating, someone close being hurt. What stops a drifter: the money running out, something happening at home, the plateau. All of it points toward the middle', ''.join(b), u)
