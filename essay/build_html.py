"""Build the essay pages from the part files (part-1-rational.md, part-2-spiritual.md).

    python prep_images.py            # once, makes img/*.jpg|png
    python build_html.py             # writes every part's .html (self-contained, images inside)
    python build_html.py --part 2    # only one part
    python build_html.py --fragment  # same pages without doctype/head/body (for publishing as an Artifact)

Edit the text in the .md file, then rebuild. Figures and portraits are placed by the
paragraph-start rules in rules1() and rules2(): the key is the first words of the paragraph.
"""
import base64
import html
import io
import os
import re
import sys

from PIL import Image

import figs2 as F
import figs3 as F3
import figs4 as F4
import figs5 as F5
import figs6 as F6

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'img')


# ---------------------------------------------------------------- images
def find_img(key):
    for ext in ('jpg', 'png'):
        p = os.path.join(IMG, f'{key}.{ext}')
        if os.path.exists(p):
            return p
    raise FileNotFoundError(key)


_cache = {}


def uri(key, size=240):
    k = (key, size)
    if k in _cache:
        return _cache[k]
    p = find_img(key)
    im = Image.open(p)
    has_alpha = im.mode == 'RGBA' and im.getextrema()[3][0] < 250
    if key in ('scooby', 'teacher', 'garden', 'stillness'):  # keep the picture's own proportions
        im = im.convert('RGB')
    else:
        im = im.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    if has_alpha:
        im.save(buf, 'PNG', optimize=True)
        mime = 'image/png'
    else:
        im.convert('RGB').save(buf, 'JPEG', quality=84, optimize=True)
        mime = 'image/jpeg'
    data = 'data:%s;base64,%s' % (mime, base64.b64encode(buf.getvalue()).decode())
    _cache[k] = data
    return data


# ---------------------------------------------------------------- text
def smart(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'(^|[\s(\[])"', lambda m: m.group(1) + '“', s)
    s = s.replace('"', '”')
    s = re.sub(r"(^|[\s(\[“])'", lambda m: m.group(1) + '‘', s)
    s = s.replace("'", '’')
    return s


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# ---------------------------------------------------------------- components
def who(key, name, room, size=104):
    return (f'<figure class="who {room}"><img src="{uri(key)}" alt="{html.escape(name)}" '
            f'width="{size}" height="{size}" loading="lazy"><figcaption>{html.escape(name)}</figcaption></figure>')


def item(figs, para_html):
    return f'<div class="item">{figs}{para_html}</div>'


def row(people):
    inner = ''.join(who(k, n, r) for k, n, r in people)
    return f'<figure class="row">{inner}</figure>'


def svg_cross():
    x0, x1, y0, y1 = 90, 620, 20, 470
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    quads = [
        ('default', x0, my, mx - x0, y1 - my, 'Default', 'low BE · low DO', ['squidward', 'costanza'], y1 - 42),
        ('driven', mx, my, x1 - mx, y1 - my, 'Driven', 'low BE · high DO', ['carrey', 'phelps', 'biles'], y1 - 42),
        ('drifting', x0, y0, mx - x0, my - y0, 'Drifting', 'high BE · low DO', ['dude', 'phoebe'], my - 42),
        ('high', mx, y0, x1 - mx, my - y0, 'High agency', 'high BE · high DO', ['malala', 'aurelius', 'parks'], my - 42),
    ]
    o = ['<svg class="chart" viewBox="0 0 660 560" role="img" aria-label="The cross: DO runs left to right, BE bottom to top, four rooms">']
    for room, qx, qy, qw, qh, title, sub, faces, cy in quads:
        o.append(f'<rect class="q {room}" x="{qx}" y="{qy}" width="{qw}" height="{qh}"/>')
        o.append(f'<text class="qt {room}" x="{qx + 16}" y="{qy + 34}">{title}</text>')
        o.append(f'<text class="mono" x="{qx + 16}" y="{qy + 54}">{sub}</text>')
        for i, f in enumerate(faces):
            cx = qx + 40 + i * 60
            o.append(f'<circle class="ring {room}" cx="{cx}" cy="{cy}" r="26"/>')
            o.append(f'<clipPath id="c-{f}"><circle cx="{cx}" cy="{cy}" r="24"/></clipPath>')
            o.append(f'<image href="{uri(f, 96)}" x="{cx - 24}" y="{cy - 24}" width="48" height="48" clip-path="url(#c-{f})" preserveAspectRatio="xMidYMid slice"/>')
    # axes
    ay = y1 + 14
    ax = x0 - 14
    o.append(f'<path class="axis" d="M{x0} {ay} H{x1}"/><path class="axis" d="M{x1 - 8} {ay - 5} L{x1} {ay} L{x1 - 8} {ay + 5}"/>')
    o.append(f'<path class="axis" d="M{ax} {y1} V{y0}"/><path class="axis" d="M{ax - 5} {y0 + 8} L{ax} {y0} L{ax + 5} {y0 + 8}"/>')
    o.append(f'<text class="mono" x="{x0}" y="{y1 + 40}">things happen to me</text>')
    o.append(f'<text class="mono" x="{x1}" y="{y1 + 40}" text-anchor="end">I make things happen</text>')
    o.append(f'<text class="axt" x="{mx}" y="{y1 + 66}" text-anchor="middle">DO</text>')
    o.append(f'<text class="mono" transform="rotate(-90 {x0 - 36} {y1})" x="{x0 - 36}" y="{y1}">braced · elsewhere</text>')
    o.append(f'<text class="mono" transform="rotate(-90 {x0 - 36} {y0})" x="{x0 - 36}" y="{y0}" text-anchor="end">released · here</text>')
    o.append(f'<text class="axt" transform="rotate(-90 {x0 - 62} {my})" x="{x0 - 62}" y="{my}" text-anchor="middle">BE</text>')
    o.append('</svg>')
    return ''.join(o)


def svg_line():
    x0, x1, y0, y1 = 80, 560, 20, 500
    s = x1 - x0

    def px(v):
        return x0 + v / 100 * s

    def py(v):
        return y1 - v / 100 * s

    o = ['<svg class="chart" viewBox="0 0 620 590" role="img" aria-label="The line of harmony: equal BE and DO, with Driven below it and Drifting above it">']
    o.append(f'<polygon class="q driven" points="{x0},{y1} {x1},{y1} {x1},{y0}"/>')
    o.append(f'<polygon class="q drifting" points="{x0},{y1} {x0},{y0} {x1},{y0}"/>')
    o.append(f'<rect class="frame" x="{x0}" y="{y0}" width="{s}" height="{s}"/>')
    o.append(f'<path class="diag" d="M{x0} {y1} L{x1} {y0}"/>')
    for v in (30, 70):
        o.append(f'<circle class="dot high" cx="{px(v)}" cy="{py(v)}" r="7"/>')
        o.append(f'<text class="mono b" x="{px(v) + 14}" y="{py(v) + 5}">{v} and {v}</text>')
    o.append(f'<text class="qt driven" x="{x1 - 16}" y="{y1 - 62}" text-anchor="end">Below the line</text>')
    o.append(f'<text class="mono" x="{x1 - 16}" y="{y1 - 42}" text-anchor="end">DO runs ahead of BE</text>')
    o.append(f'<text class="mono" x="{x1 - 16}" y="{y1 - 26}" text-anchor="end">Driven</text>')
    o.append(f'<text class="qt drifting" x="{x0 + 16}" y="{y0 + 40}">Above the line</text>')
    o.append(f'<text class="mono" x="{x0 + 16}" y="{y0 + 60}">BE runs ahead of DO</text>')
    o.append(f'<text class="mono" x="{x0 + 16}" y="{y0 + 76}">Drifting</text>')
    o.append(f'<text class="mono b" transform="rotate(-45 {px(52)} {py(52)})" x="{px(52)}" y="{py(52) - 12}" text-anchor="middle">the line of harmony</text>')
    o.append(f'<text class="mono" x="{px(50)}" y="{y1 + 34}" text-anchor="middle">DO →</text>')
    o.append(f'<text class="mono" transform="rotate(-90 {x0 - 20} {py(50)})" x="{x0 - 20}" y="{py(50)}" text-anchor="middle">BE →</text>')
    o.append('</svg>')
    return ''.join(o)


def mini_square(do, be, room, label, area):
    w, h = do, be
    return (f'<figure class="sq"><svg viewBox="0 0 100 100" role="img" aria-label="{html.escape(label)}">'
            f'<rect class="frame" x="0.5" y="0.5" width="99" height="99"/>'
            f'<rect class="fillrect {room}" x="0.5" y="{100 - h - 0.5}" width="{max(w - 1, 1)}" height="{max(h - 1, 1)}"/></svg>'
            f'<figcaption><b>{html.escape(label)}</b><span>{do} × {be} = {area}</span></figcaption></figure>')


def squares():
    items = [
        mini_square(10, 10, 'default', 'Default', '100'),
        mini_square(100, 10, 'driven', 'Driven at the wall', '1,000'),
        mini_square(10, 100, 'drifting', 'Drifting, the mirror', '1,000'),
        mini_square(100, 100, 'high', 'The corner', '10,000'),
    ]
    return '<div class="squares">' + ''.join(items) + '</div>'


def svg_swing():
    x0, x1, y0, y1 = 70, 590, 20, 500
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    # unit vectors: d runs up the line of harmony, n points to the Driven side
    dx, dy = 520 / 709.3, -480 / 709.3
    nx, ny = -dy, dx
    amps = [190, -175, 155, -135, 110, -85, 60, -40, 20, 0]
    pts = []
    for k, a in enumerate(amps):
        b = -140 + k * 24
        pts.append((mx + a * nx + b * dx, my + a * ny + b * dy))
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    ex, ey = pts[-1]
    o = ['<svg class="chart" viewBox="0 0 620 560" role="img" aria-label="A swing that narrows: a life traced across Driven and Drifting, closing in on the line, then climbing it">']
    o.append(f'<rect class="q default" x="{x0}" y="{my}" width="{mx - x0}" height="{y1 - my}"/>')
    o.append(f'<rect class="q driven" x="{mx}" y="{my}" width="{x1 - mx}" height="{y1 - my}"/>')
    o.append(f'<rect class="q drifting" x="{x0}" y="{y0}" width="{mx - x0}" height="{my - y0}"/>')
    o.append(f'<rect class="q high" x="{mx}" y="{y0}" width="{x1 - mx}" height="{my - y0}"/>')
    o.append(f'<path class="diag" d="M{x0} {y1} L{x1} {y0}"/>')
    o.append(f'<path class="swing" d="{d}"/>')
    # the climb is wavy too: the swing keeps shrinking until the peak
    import math
    px_, py_ = 548.0, 52.0
    vx, vy = px_ - ex, py_ - ey
    L = math.hypot(vx, vy)
    ux, uy = vx / L, vy / L
    wx, wy = -uy, ux
    steps = 160
    wave = []
    for i in range(steps + 1):
        t = i / steps
        off = 30 * (1 - t) ** 1.15 * math.sin(2 * math.pi * 4.5 * t)
        wave.append((ex + vx * t + wx * off, ey + vy * t + wy * off))
    wd = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in wave)
    o.append(f'<path class="climb" d="{wd}"/>')
    o.append('<path class="climbhead" d="M536 48 L552 48 L552 64"/>')
    for i, (x, y) in enumerate(pts):
        o.append(f'<circle class="dot ink" cx="{x:.1f}" cy="{y:.1f}" r="{5 if i == 0 else 3.5}"/>')
    p0, p1, p2 = pts[0], pts[1], pts[2]
    o.append(f'<text class="mono b halo" x="{p0[0] + 14:.1f}" y="{p0[1] + 4:.1f}">the wall: all DO</text>')
    o.append(f'<text class="mono b halo" x="{p1[0] - 4:.1f}" y="{p1[1] - 14:.1f}">burnout, then "screw this"</text>')
    o.append(f'<text class="mono b halo" x="{x1 - 8}" y="{p2[1] + 12:.1f}" text-anchor="end">full business, never again</text>')
    o.append(f'<text class="mono b halo" x="{mx + 120}" y="{my + 40}">the swing narrows</text>')
    o.append(f'<text class="mono b halo" x="{x1 - 8}" y="{y0 + 210}" text-anchor="end">then the climb</text>')
    o.append(f'<text class="mono" x="{mx}" y="{y1 + 34}" text-anchor="middle">DO \u2192</text>')
    o.append(f'<text class="mono" transform="rotate(-90 {x0 - 20} {my})" x="{x0 - 20}" y="{my}" text-anchor="middle">BE \u2192</text>')
    o.append('</svg>')
    return ''.join(o)


def svg_zoom():
    x0, x1, y0, y1 = 70, 590, 30, 550
    s = x1 - x0
    small = s * 0.1
    o = ['<svg class="chart" viewBox="0 0 620 610" role="img" aria-label="Zoom out ten times: the 100 by 100 square becomes a small box inside a 1,000 by 1,000 map">']
    o.append(f'<rect class="q high" x="{x0}" y="{y0}" width="{s}" height="{s}"/>')
    o.append(f'<rect class="frame" x="{x0}" y="{y0}" width="{s}" height="{s}"/>')
    o.append(f'<rect class="fillrect high solid" x="{x0}" y="{y1 - small}" width="{small}" height="{small}"/>')
    o.append(f'<path class="leader" d="M{x0 + small} {y1 - small} L{x0 + 150} {y1 - 120}"/>')
    o.append(f'<text class="mono b" x="{x0 + 156}" y="{y1 - 120}">this part\'s map</text>')
    o.append(f'<text class="mono" x="{x0 + 156}" y="{y1 - 102}">100 × 100 = 10,000</text>')
    o.append(f'<text class="big" x="{(x0 + x1) / 2}" y="{y0 + 210}" text-anchor="middle">1,000 × 1,000</text>')
    o.append(f'<text class="big" x="{(x0 + x1) / 2}" y="{y0 + 262}" text-anchor="middle">= 1,000,000</text>')
    o.append(f'<text class="qt high" x="{(x0 + x1) / 2}" y="{y0 + 312}" text-anchor="middle">full human potential</text>')
    o.append(f'<text class="mono" x="{x0}" y="{y1 + 24}">0</text>')
    o.append(f'<text class="mono" x="{x1}" y="{y1 + 24}" text-anchor="end">1,000</text>')
    o.append(f'<text class="mono" x="{(x0 + x1) / 2}" y="{y1 + 24}" text-anchor="middle">DO →</text>')
    o.append(f'<text class="mono" x="{x0 - 12}" y="{y0 + 12}" text-anchor="end">1,000</text>')
    o.append(f'<text class="mono" transform="rotate(-90 {x0 - 34} {(y0 + y1) / 2})" x="{x0 - 34}" y="{(y0 + y1) / 2}" text-anchor="middle">BE →</text>')
    o.append('</svg>')
    return ''.join(o)


def figure(inner, caption, cls=''):
    return f'<figure class="fig {cls}">{inner}<figcaption>{caption}</figcaption></figure>'


# ---------------------------------------------------------------- placement rules
# paragraph-start text -> (before_html_fn or None, after_html_fn or None)
def rules1():
    return {
        'Draw them as a cross.': dict(after=figure(svg_cross(), 'The cross. DO runs left to right, BE runs bottom to top. Each room with the people who will show up in it.')),
        'Squidward is the most extreme': dict(who=[('squidward', 'Squidward', 'default')]),
        'George Costanza is the exit story': dict(who=[('costanza', 'George Costanza', 'default')]),
        'Hank Hill is that corner': dict(before=row([('hank', 'Hank Hill', 'default'), ('jim', 'Jim Halpert', 'default'), ('pam', 'Pam Beesly', 'default')])),
        'Jim Carrey is one answer': dict(who=[('carrey', 'Jim Carrey', 'driven')]),
        'Michael Phelps is the same story': dict(who=[('phelps', 'Michael Phelps', 'driven')]),
        'Simone Biles is the most decorated': dict(who=[('biles', 'Simone Biles', 'driven')]),
        'The best-known example is the Dude': dict(who=[('dude', 'The Dude', 'drifting')]),
        'Phoebe from Friends': dict(who=[('phoebe', 'Phoebe Buffay', 'drifting')]),
        'John Welwood, an American psychologist': dict(who=[('welwood', 'John Welwood', 'neutral')]),
        'Malala Yousafzai kept going': dict(who=[('malala', 'Malala Yousafzai', 'high')]),
        'Marcus Aurelius ran the Roman Empire': dict(who=[('aurelius', 'Marcus Aurelius', 'high')]),
        'Rosa Parks is a good one': dict(who=[('parks', 'Rosa Parks', 'high')]),
        'Picture the whole chart as a square, 10,000': dict(after=figure(squares(), 'The same square, four ways. Width is DO, height is BE, the shaded part is the area a person takes up.', 'plain')),
        'On the line, what you\'re free to want': dict(after=figure(svg_line(), 'The line of harmony. Position along it says how far you have come. Distance from it says how much is leaking.')),
        'Learning to walk on two legs': dict(after=figure(svg_swing(), 'A swing that narrows, then the climb, which stays wavy until the peak. Illustration, not data.')),
        'Zoom out by ten': dict(after=figure(svg_zoom(), 'Zoom out by ten. The whole square we have been using is the small box in the corner.')),
        'Picture the steering wheel of your life.': dict(after=figure(F.fig_wheel(), 'Hands on the wheel, or in the back seat.')),
        'Asking is a quiet one': dict(after=figure(F.icons_html(), 'Five quiet kinds of DO.', 'plain')),
        'It matters even if you couldn': dict(after=figure(F.fig_shelf(), 'The tax on seeing solutions: most of the shelf is ruled out before you look.')),
        'Here is the connection to being here.': dict(after=figure(F.fig_attention(), 'Where your attention is, as opposed to where your body is.')),
        'The turbulence comes from walking on two legs.': dict(after=figure(F.fig_legs(), 'Three ways to move. The DO leg is vermilion, the BE leg is blue.')),
        'Here is why the turbulence is worth it': dict(after=figure(F.fig_loop(), 'The two legs feed each other.')),
        'A quick way to find your own examples': dict(after=figure(F.fig_jail(), 'The jail-cell test.')),
        'The Soviet physiologist Pyotr Anokhin': dict(li_after=figure(F.fig_anokhin(), 'Anokhin\'s functional system, simplified: a goal is a model of the result, and the result is compared with it.')),
        'Viktor Frankl, a psychiatrist': dict(who=[('frankl', 'Viktor Frankl', 'neutral')]),
        'The lab has looked at this too': dict(after=figure(F.fig_studies(), 'Left: a randomized field experiment. Right: a review of ten long-term studies, which shows an association, not a cause. Read both as a direction.')),
        'Picture someone who freezes': dict(after=figure(F.fig_scales(), 'The fear is a vote. A bigger reason is a bigger vote.')),
        'A lot of the tension is also made of self-monitoring': dict(after=figure(F.fig_spot(), 'The spotlight effect (Gilovich and colleagues, 2000): we overestimate how much others notice us.')),
        'Reasons also outlast goals.': dict(after=figure(F.fig_finish(), 'Goals about you end. Reasons about others keep going.')),
        'What gets someone across the middle on purpose is a pull.': dict(after=figure(F.fig_pushpull(), 'Pushes and a pull.')),
        'The extreme version of this room': dict(after=figure(F.fig_tv(), 'Aware of everything, in none of it.')),
        'Default has a nice corner too': dict(who=[('thoreau', 'Henry David Thoreau', 'neutral')]),
        'With my personality tendencies': dict(after=figure(F.fig_week(), 'Work all week, study on the weekends, with a constant background tension of not being good enough.')),
        "I don't want to knock this room.": dict(after=figure(F.fig_wall(), 'When a problem does not move, push harder in the same direction.')),
        'Top left: released and passive': dict(after=figure(F.fig_hammock(), 'Where life rarely pushes you from the outside.')),
        'The trap is that it feels good': dict(after=figure(F.fig_gym(), 'Very peaceful. Much calm. Nobody gets hurt and nobody gets stronger.')),
        'So what do you get for walking on both legs?': dict(after=figure(F.fig_inout(), 'The top right, from the inside and from the outside.')),
        'Take Stoicism, because the internet version is so popular.': dict(after=figure(F.fig_stoic(), 'Stoicism, misread and as practiced.')),
        "For a drifter I've noticed three things.": dict(after=figure(F.fig_stops(), 'What stops each room, and where it points: the middle.')),
        'At the far corner of the chart is the peak': dict(after=figure(F.icons_flow_html(), 'Different rooms, same visit.', 'plain')),
        'Put it together.': dict(after=figure(F.fig_footsteps(), 'Walking in step: the lazy leg catches up, again and again.')),
        'The reason is inertia.': dict(after=figure(F.fig_inertia(), 'Inertia.')),
        'There\'s a name for what Carrey and Phelps ran into': dict(who=[('benshahar', 'Tal Ben-Shahar', 'neutral')]),
    }


def rules2a():
    return {
        "There's a word I could have used instead": dict(after=figure(F3.fig_door(), 'The door: a ring in the middle of the chart. Some people circle it for years, and some cross.')),
        'Default protects it.': dict(after=figure(F3.fig_rooms(), 'Four rooms, one assumption underneath.')),
        'You can check the body part of this right now': dict(after=figure(F3.fig_fist(), 'The same person, tensed and then released.')),
        'A child lies in a dark room': dict(after=figure(F3.fig_dark(), 'The room is the same in both pictures.')),
        'People have been writing about this for far longer': dict(after=figure(F3.fig_names(), 'Names from different traditions for the far side of the map. They are not the same claim, and they point in roughly the same direction.')),
        'Start with the border itself.': dict(after=figure(F3.fig_rubber(), 'The rubber hand illusion. The felt border of the body is something the brain works out, and it can be moved.')),
    }


def rules0():
    return {
        'Everything in this book rests on what I learned': dict(after=figure(
            f'<img class="pic" src="{uri("teacher")}" width="720" height="900" loading="lazy" '
            'alt="Two men standing side by side outdoors, the author and his teacher, Genadiy Givin">',
            'My teacher, Genadiy Givin, and I.', 'photo')),
    }


PART0_CSS = '.fig .pic{display:block;width:100%;max-width:26rem;height:auto;margin:0 auto;border-radius:10px;border:1px solid var(--rule)}'


def rules2():
    return {
        'From these three clauses I want to build the rest': dict(after=figure(F4.fig_chain(), 'The chain. The arrows show the order. The tags on the right give the premises each step uses, which are not always the step above.')),
        'The second view sits at the other extreme': dict(after=figure(F4.fig_views(), 'Two assumptions at opposite ends. Neither can be observed from outside, since the observing is done by the same mind.')),
        'Under the axiom, you and I are programs.': dict(after=figure(F4.fig_cpu(), 'Far apart on the screen, side by side in the machine. The distance is a property of the drawing.')),
        'The body holds the limits in place.': dict(after=figure(F4.fig_wall(), 'The wall, as it shows in the body. Hold less of it and you sit higher on BE.')),
        'How it carries on is where the traditions part': dict(after=figure(F4.fig_lives(), 'What a life gathers is kept and carried on, whichever form the traditions give it.')),
        'If we are one, there is nobody else.': dict(after=figure(F4.fig_fingers(), 'Karma, with the courtroom taken out.')),
        'My answer is that it takes doing less.': dict(after=F6.widget()),
        'Your own body does it too.': dict(after=figure(F5.JOKES['fig_cell'](), 'Every cell carries the whole plan and uses a small part of it. The rest is switched off and kept.')),
        'That gives suffering a job.': dict(after=figure(F5.fig_warning(), 'Suffering as the warning light on the dashboard. The tape is also an option.')),
        "That's also why love is strongest": dict(after=figure(F5.fig_needlove(), 'Need says, I need you so that I feel whole. Love says, you are part of what I am.')),
        'Somewhere there is a bottom point': dict(after=figure(F5.fig_turn(), 'Two halves of one game. Past the bottom point the same moves stop paying, and a step toward unity starts to.')),
        "That something can't be the body": dict(after=figure(F5.fig_lamps(), 'A lamp lit from another lamp.')),
        'Spend two hours with someone': dict(after=figure(F5.fig_hours(), 'The same two hours, on guard and with an old friend.')),
        'Here is the picture I use. Take a piece of cloth': dict(after=figure(F5.fig_cloth(), 'One cloth. The jewel you lift rises first, and the nearest ones rise with it.')),
        "Under the axiom it can't really work that way": dict(after=figure(F5.fig_mill(), 'A tank, and a mill on a river. The mill does not drink the river. Its job is to let the water through.')),
        'If one structure sits behind all this, why': dict(after=figure(F5.fig_paths(), 'A path is drawn for particular people at a particular time, and the paths meet at the same place.')),
        'Until then, one question': dict(after=figure(F5.fig_border(), 'Where, right now, does the border of you sit?')),
    }


def photo(key, alt, caption):
    return figure(f'<img class="pic" src="{uri(key)}" width="800" height="800" loading="lazy" alt="{alt}">', caption, 'photo')


def rules3():
    return {
        'The order goes from what only you': dict(after=figure(F5.fig_eight(), 'Eight conditions, in the order of this part.')),
        'Think of a time you really decided': dict(after=figure(F5.JOKES['fig_yes'](), 'Before the yes, every day is a small debate. After it, the days line up.')),
        'Anything that moves needs two things': dict(after=figure(F5.fig_cars(), 'The wish is the fuel, and a goal is the steering.')),
        'Behind each goal sits a reason': dict(after=figure(F5.fig_goalreason(), 'The goal can be small as long as the reason is bigger than you.')),
        'Keep it light, and keep it yours': dict(after=figure(F5.JOKES['fig_streak'](), 'A frame you can keep. When a day slips, pick it up the next day.')),
        'The second job is letting go': dict(after=figure(F5.fig_clamps(), 'Attention held on a clamp like a flashlight on one spot, with no pushing.')),
        "Part two said the belief that I'm separate": dict(after=figure(F5.JOKES['fig_jobs'](), 'The three jobs of attention.')),
        "Underneath all three there's a plain skill": dict(after=figure(F5.fig_apart(), 'What usually arrives glued together starts to come apart.')),
        'Prayer is the same attention': dict(after=figure(F5.JOKES['fig_ditch'](), "Prayers alone don't bring rain, and someone has to dig the ditches for it.")),
        'It starts with the people closest to you,': dict(after=figure(F5.JOKES['fig_circles'](), 'It starts with the people closest to you, and the circle widens from there.')),
        'Then we had an enormous fight.': dict(after=figure(F5.fig_lever(), 'The lever was so rusty it barely moved. After about ten minutes it moved.')),
        'When someone harms you, you react': dict(after=figure(F5.fig_samestep(), 'The same step away can be a clear choice or a flinch.')),
        'This condition matters more now': dict(after=figure(F5.JOKES['fig_weekend'](), 'A strong weekend, on your own and with people you see every week. An illustration, not data.')),
        'There will be moments, plenty of them': dict(after=figure(F5.fig_emotion(), 'Decide nothing while the emotion is there. Look again with a clear head, and take seriously what is still there.')),
        'Stillness is the simplest form of this': dict(after=photo('stillness', 'The author sitting cross-legged with eyes closed, with his team meditating around him', 'Most days I sit like this two or three times. The beard is not part of the method.')),
    }


# ---------------------------------------------------------------- build
CSS = r"""
:root{
  --paper:#FAF7F1; --ink:#1F1C17; --muted:#6B6457; --rule:#E2DBCC; --grid:#EFE9DD; --card:#FFFDF9;
  --side:#F3EEE4; --hover:#EAE3D5; --accent:#0C7A5E;
  --head:'Literata',Georgia,'Times New Roman',serif;
  --default:#6B7A99; --driven:#D2502F; --drifting:#4A66D6; --high:#0C8A6A;
  --k-trad:#3E5CC0; --k-study:#0C8A6A; --k-look:#5F6E8E; --k-life:#B5602A; --k-story:#8A4BAE;
  --display:'Bricolage Grotesque','Segoe UI',system-ui,sans-serif;
  --body:'Literata',Georgia,'Times New Roman',serif;
  --mono:'IBM Plex Mono',ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#16140F; --ink:#ECE6DA; --muted:#A99F8E; --rule:#2F2A21; --grid:#1D1A14; --card:#1E1B15;
  --side:#1B1813; --hover:#28241C; --accent:#31C79F;
  --default:#8E9BBA; --driven:#F0724F; --drifting:#7B93F0; --high:#31C79F;
  --k-trad:#8FA4F2; --k-study:#3CCBA4; --k-look:#A3AECA; --k-life:#E89A62; --k-story:#C79AE6; color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#16140F; --ink:#ECE6DA; --muted:#A99F8E; --rule:#2F2A21; --grid:#1D1A14; --card:#1E1B15;
  --side:#1B1813; --hover:#28241C; --accent:#31C79F;
  --default:#8E9BBA; --driven:#F0724F; --drifting:#7B93F0; --high:#31C79F;
  --k-trad:#8FA4F2; --k-study:#3CCBA4; --k-look:#A3AECA; --k-life:#E89A62; --k-story:#C79AE6; color-scheme:dark}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:1.15rem;line-height:1.72;overflow-x:clip;font-optical-sizing:auto;text-rendering:optimizeLegibility}
.hero{position:relative;padding:clamp(3rem,9vh,6rem) 1rem 1rem;text-align:center}
.hero-in{position:relative;max-width:38rem;margin:0 auto}
.kicker{font-family:var(--mono);font-size:.78rem;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin:0 0 1.1rem}
h1{font-family:var(--head);font-weight:600;font-size:clamp(2.9rem,10vw,4.6rem);line-height:1.02;letter-spacing:-.02em;margin:0;text-wrap:balance}
.lede{font-family:var(--head);font-style:italic;font-size:1.3rem;line-height:1.5;margin:1.3rem auto 0;max-width:30rem;color:var(--muted);text-wrap:balance}
.meta{font-family:var(--mono);font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:1.3rem 0 0}
.orn{display:flex;align-items:center;justify-content:center;gap:.9rem;margin:2.4rem auto 0;max-width:14rem}
.orn span{flex:1;height:1px;background:var(--rule)}
.orn i{width:.5rem;height:.5rem;transform:rotate(45deg);border:1px solid var(--accent)}
main{padding:0 1rem 4rem}
.col{max-width:38rem;margin:2.5rem auto 0;hyphens:auto;-webkit-hyphens:auto}
.col p.first::first-letter{font-family:var(--head);font-weight:600;font-size:2.7em;line-height:1;margin-right:.04em;color:var(--accent)}
.turn{max-width:38rem;margin:4rem auto 2.5rem;display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.turn a{display:flex;flex-direction:column;gap:.25rem;padding:1rem 1.15rem;border:1px solid var(--rule);border-radius:12px;background:var(--card);text-decoration:none;color:var(--ink);transition:border-color .15s,transform .15s}
.turn a:hover{border-color:var(--accent);transform:translateY(-1px)}
.turn a span{font-family:var(--mono);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.turn a b{font-family:var(--head);font-weight:600;font-size:1.08rem;line-height:1.3}
.turn .next{grid-column:2;text-align:right}
@media (max-width:34rem){.turn{grid-template-columns:1fr}.turn .next{grid-column:1}}
.toc{font-family:var(--mono);font-size:.82rem;line-height:1.9;margin:0 0 2.5rem;padding:1rem 0;border-block:1px solid var(--rule)}
.toc a{color:var(--muted);text-decoration:none;margin-right:1rem;white-space:nowrap}
.toc a:hover{color:var(--ink);text-decoration:underline}
h2{font-family:var(--head);font-weight:600;font-size:clamp(1.75rem,5vw,2.25rem);line-height:1.15;letter-spacing:-.015em;margin:4.2rem 0 1.2rem;text-wrap:balance;scroll-margin-top:4.5rem}
h2::before{content:"";display:block;width:2.2rem;height:2px;background:var(--accent);margin:0 0 1.1rem}
h3.room{font-family:var(--head);font-weight:600;font-size:1.55rem;margin:2.6rem 0 .9rem;display:flex;align-items:center;gap:.6rem}
h3.room .dot{width:.9rem;height:.9rem;border-radius:3px;background:currentColor}
h3.room.default{color:var(--default)}h3.room.driven{color:var(--driven)}h3.room.drifting{color:var(--drifting)}h3.room.high{color:var(--high)}
p{margin:0 0 1.15rem}
.item{display:flow-root}
.item p:last-child{margin-bottom:1.15rem}
figure{margin:0}
.who{float:left;width:6.8rem;margin:.2rem 1.2rem .5rem 0;text-align:center}
.who img{display:block;width:6.5rem;height:6.5rem;border-radius:50%;object-fit:cover;background:var(--card);border:3px solid var(--rule)}
.who.default img{border-color:var(--default)}.who.driven img{border-color:var(--driven)}.who.drifting img{border-color:var(--drifting)}.who.high img{border-color:var(--high)}
.who figcaption{font-family:var(--mono);font-size:.7rem;line-height:1.3;color:var(--muted);margin-top:.35rem}
.row{display:flex;flex-wrap:wrap;justify-content:center;gap:.4rem 1.4rem;margin:1.6rem 0}
.row .who{float:none;margin:0}
.fig{width:min(54rem,calc(100vw - 2rem));position:relative;left:50%;transform:translateX(-50%);margin:2.2rem 0}
.fig.plain,.fig.photo{width:min(40rem,100%);left:0;transform:none}
.fig svg.chart{display:block;width:100%;max-width:38rem;height:auto;margin:0 auto}
.fig figcaption{font-family:var(--mono);font-size:.78rem;line-height:1.5;color:var(--muted);text-align:center;margin:.8rem auto 0;max-width:34rem}
.fig .scooby{display:block;width:100%;height:auto;border-radius:10px;border:1px solid var(--rule)}
.chart text{font-family:var(--mono);font-size:12.5px;fill:var(--muted)}
.chart text.mono.b{fill:var(--ink);font-weight:500}
.chart text.halo{paint-order:stroke;stroke:var(--paper);stroke-width:5px;stroke-linejoin:round}
.chart text.qt{font-family:var(--display);font-weight:800;font-size:22px}
.chart text.qt.default{fill:var(--default)}.chart text.qt.driven{fill:var(--driven)}.chart text.qt.drifting{fill:var(--drifting)}.chart text.qt.high{fill:var(--high)}
.chart text.axt{font-family:var(--display);font-weight:800;font-size:26px;fill:var(--ink)}
.chart text.big{font-family:var(--display);font-weight:800;font-size:38px;fill:var(--ink)}
.chart .q{stroke:var(--rule);stroke-width:1;fill-opacity:.14}
.chart .q.default,.chart .ring.default{fill:var(--default)}.chart .q.driven{fill:var(--driven)}.chart .q.drifting{fill:var(--drifting)}.chart .q.high{fill:var(--high)}
.chart .ring{fill:none;stroke-width:3}
.chart .ring.default{stroke:var(--default);fill:none}.chart .ring.driven{stroke:var(--driven)}.chart .ring.drifting{stroke:var(--drifting)}.chart .ring.high{stroke:var(--high)}
.chart .axis{stroke:var(--ink);stroke-width:1.6;fill:none;stroke-linecap:round;stroke-linejoin:round}
.chart .frame{fill:none;stroke:var(--ink);stroke-width:1.4}
.chart .diag{stroke:var(--ink);stroke-width:1.6;stroke-dasharray:6 5;fill:none}
.chart .swing{fill:none;stroke:var(--ink);stroke-width:2;stroke-linejoin:round}
.chart .climb{fill:none;stroke:var(--high);stroke-width:4;stroke-linecap:round}
.chart .climbhead{fill:none;stroke:var(--high);stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.chart .leader{stroke:var(--ink);stroke-width:1.2;fill:none}
.chart .dot.high{fill:var(--high)}.chart .dot.ink{fill:var(--ink)}
.chart .fillrect.high{fill:var(--high)}
.fillrect.default{fill:var(--default)}.fillrect.driven{fill:var(--driven)}.fillrect.drifting{fill:var(--drifting)}.fillrect.high{fill:var(--high)}
.fillrect.soft{fill-opacity:.4}.fillrect.mid{fill-opacity:.7}.fillrect.solid{fill-opacity:1}
.squares{display:grid;grid-template-columns:repeat(4,1fr);gap:1.4rem 1rem;max-width:30rem;margin:0 auto}
@media (max-width:30rem){.squares{grid-template-columns:repeat(2,1fr)}.who{width:5.2rem}.who img{width:5rem;height:5rem}}
.sq svg{display:block;width:100%;max-width:8.5rem;margin:0 auto;background:var(--card)}
.sq .frame{fill:none;stroke:var(--ink);stroke-width:1.4}
.sq figcaption{display:flex;flex-direction:column;align-items:center;text-align:center;font-family:var(--mono);font-size:.74rem;line-height:1.4;margin-top:.5rem;color:var(--muted)}
.sq figcaption b{color:var(--ink);font-weight:500}
.chart .st{fill:none;stroke:var(--ink);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.chart .stm{fill:none;stroke:var(--muted);stroke-width:1.8;stroke-linecap:round}
.chart .stm2{fill:none;stroke:var(--muted);stroke-width:2.4;stroke-linecap:round}
.chart .stg{fill:none;stroke:var(--high);stroke-width:2.6;stroke-linecap:round}
.chart .hi{fill:none;stroke:var(--high);stroke-width:2.4;stroke-linecap:round}
.chart .dash{stroke-dasharray:5 5}
.chart .card{fill:var(--card);stroke:var(--ink);stroke-width:1.8;stroke-linejoin:round}
.chart .cardm{fill:var(--card);stroke:var(--rule);stroke-width:1.5}
.chart .cardhi{fill:var(--card);stroke:var(--high);stroke-width:2.4}
.chart .room{fill:var(--card);stroke:var(--rule);stroke-width:1.5}
.chart .bubble{fill:var(--paper);stroke:var(--muted);stroke-width:1.4}
.chart .dimbox{fill:none;stroke:var(--muted);stroke-width:1.5;stroke-dasharray:5 4}
.chart .hibox{fill:var(--high);fill-opacity:.18;stroke:var(--high);stroke-width:2.2}
.chart .rim{fill:none;stroke:var(--ink);stroke-width:14}
.chart .spoke{fill:none;stroke:var(--ink);stroke-width:12;stroke-linecap:round}
.chart .fmu2{fill:var(--ink)}
.chart .fhi{fill:var(--high)}.chart .fdo{fill:var(--driven)}.chart .fmu{fill:var(--muted)}
.chart .sdo{fill:none;stroke:var(--driven);stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
.chart .sbe{fill:none;stroke:var(--drifting);stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
.chart .shi{fill:none;stroke:var(--high);stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.chart .ringm{fill:none;stroke:var(--ink);stroke-width:1.6;stroke-dasharray:6 5}
.chart .cone{fill:var(--high);fill-opacity:.14;stroke:none}
.chart .screen{fill:var(--paper);stroke:var(--rule);stroke-width:1.4}
.chart .ghost{fill-opacity:.35}
.chart text.small{font-size:11.5px}
.chart text.b{fill:var(--ink);font-weight:500}
.chart text.t{font-family:var(--display);font-weight:700;font-size:15px;fill:var(--ink)}
.chart text.ts{font-family:var(--display);font-weight:700;font-size:13px;fill:var(--ink)}
.chart text.ts.big2{font-size:28px}
.chart text.big3{font-family:var(--display);font-weight:800;font-size:28px;fill:var(--ink)}
.mk-ink{stroke:var(--ink)}.mk-hi{stroke:var(--high)}.mk-mu{stroke:var(--muted)}.mk-do{stroke:var(--driven)}
.who.neutral img{border-color:var(--muted)}
.icons{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;max-width:36rem;margin:0 auto}
@media (max-width:30rem){.icons{grid-template-columns:repeat(3,1fr)}}
.ic svg.chart.icon{display:block;width:100%;max-width:4.5rem;margin:0 auto}
.fig .ic figcaption{font-family:var(--mono);font-size:.74rem;text-align:center;margin:.4rem 0 0;color:var(--ink)}
.chart .sunf{fill:var(--high);fill-opacity:.9;stroke:var(--ink);stroke-width:1.8}
.chart .heartf{fill:var(--driven);fill-opacity:.85;stroke:var(--ink);stroke-width:1.8;stroke-linejoin:round}
.chart .foot{fill-opacity:.9}
.chart .fsoft{fill-opacity:.62}
.chart .rockf{fill:var(--muted);fill-opacity:.35;stroke:var(--ink);stroke-width:2.2;stroke-linejoin:round}
.chart text.dg2{font-family:'Comic Neue','Comic Sans MS','Chalkboard SE',cursive;font-weight:700;font-size:15px;fill:var(--ink)}
.chart text.dg2.big4{font-size:24px}
.chart text.dg2.c1{fill:var(--drifting)}.chart text.dg2.c2{fill:var(--driven)}.chart text.dg2.c3{fill:var(--high)}
.chart text.dg{font-family:'Comic Neue','Comic Sans MS','Chalkboard SE',cursive;font-weight:700;stroke:#000;stroke-width:4px;paint-order:stroke;stroke-linejoin:round}
.chart .wt{font-family:var(--display);font-weight:700;font-size:15px;fill:var(--paper)}
.chart text.faint{opacity:.65}
.chart .trunk{fill:none;stroke:var(--ink);stroke-width:7;stroke-linecap:round}
.chart .frond{fill:none;stroke:var(--high);stroke-width:5;stroke-linecap:round}
.chart .wallr{fill:var(--muted);stroke:var(--ink);stroke-width:1.8}
.chart .sdo2{fill:none;stroke:var(--driven);stroke-width:5;stroke-linecap:round}
.chart .fbe{fill:var(--drifting)}
.fig .ic figcaption span{color:var(--muted)}
.cast{display:flex;flex-wrap:wrap;justify-content:center;margin:0 0 2.4rem;padding-left:.7rem}
.cast img{width:3.4rem;height:3.4rem;border-radius:50%;object-fit:cover;border:3px solid var(--paper);margin-left:-.7rem;background:var(--card);box-shadow:0 0 0 2px var(--rule)}
.cast img.default{box-shadow:0 0 0 2px var(--default)}.cast img.driven{box-shadow:0 0 0 2px var(--driven)}.cast img.drifting{box-shadow:0 0 0 2px var(--drifting)}.cast img.high{box-shadow:0 0 0 2px var(--high)}
.cast-cap{font-family:var(--mono);font-size:.74rem;color:var(--muted);text-align:center;margin:-1.6rem 0 2.2rem}
.sources{font-size:.92rem;line-height:1.55;padding-left:1.1rem}
.say{padding-left:1.15rem;margin:0 0 1.4rem}
.slot{font-family:var(--mono);font-size:.82rem;line-height:1.5;color:var(--muted);border-left:3px solid var(--driven);padding:.5rem .8rem;margin:1.2rem 0;background:var(--card)}
details.say-fold{margin:1.4rem 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:.15rem 0}
details.say-fold.k-trad{--kc:var(--k-trad)}details.say-fold.k-study{--kc:var(--k-study)}details.say-fold.k-look{--kc:var(--k-look)}details.say-fold.k-life{--kc:var(--k-life)}details.say-fold.k-story{--kc:var(--k-story)}
details.say-fold summary{cursor:pointer;list-style:none;display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:start;gap:.85rem;padding:.95rem 0;font-size:1rem;color:var(--ink)}
details.say-fold summary::-webkit-details-marker{display:none}
details.say-fold summary:focus-visible{outline:2px solid var(--kc);outline-offset:3px;border-radius:4px}
details.say-fold .ki{width:1.35rem;height:1.35rem;color:var(--kc);margin-top:.15rem}
details.say-fold .kt{min-width:0;display:flex;flex-direction:column;gap:.15rem}
details.say-fold .kk{font-family:var(--mono);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--kc)}
details.say-fold .tt{font-family:var(--head);font-weight:600;font-size:1.1rem;line-height:1.3}
details.say-fold .tz{color:var(--muted);font-size:.95rem;line-height:1.5;margin-top:.25rem;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;-webkit-mask-image:linear-gradient(90deg,#000 70%,transparent);mask-image:linear-gradient(90deg,#000 70%,transparent)}
details.say-fold[open] .tz{display:none}
details.say-fold .pm::before{content:"+";font-family:var(--mono);font-size:1.15rem;line-height:1.3;color:var(--muted)}
details.say-fold[open]>summary .pm::before{content:"\2212"}
details.say-fold summary:hover .pm::before{color:var(--kc)}
details.say-fold .kb{border-left:2px solid var(--kc);padding-left:.9rem;margin-bottom:.8rem}
details.say-fold .say{margin-top:0}
.say li.grp{list-style:none;margin:1.3rem 0 .6rem -1.15rem;padding-left:0;font-family:var(--mono);font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.say li.grp:first-child{margin-top:.3rem}
details.say-fold .say-close{margin:1.2rem 0 .6rem}
@media print{details.say-fold>*{display:block}details.say-fold .tz{display:none}}
.say li{margin-bottom:.7rem;padding-left:.2rem}
.say li::marker{color:var(--muted)}
.sources li{margin-bottom:.7rem;overflow-wrap:anywhere}
h4{font-family:var(--mono);font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:1.6rem 0 .8rem;font-weight:500}
footer{max-width:38rem;margin:0 auto;padding:1.5rem 0 0;border-top:1px solid var(--rule);font-family:var(--mono);font-size:.74rem;line-height:1.6;color:var(--muted)}
a{color:var(--high)}
.contact{margin:1.5rem 0 1rem}
.contact-form{display:grid;gap:1.1rem;margin-top:1rem}
.contact-form label{display:grid;gap:.35rem;font-family:var(--mono);font-size:.78rem;color:var(--muted)}
.contact-form .hint{font-size:.78rem}
.contact-form input,.contact-form textarea{font:inherit;font-family:var(--body,inherit);font-size:1rem;color:var(--ink);background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:.6rem .7rem;width:100%;box-sizing:border-box}
.contact-form textarea{min-height:7.5rem;line-height:1.5;resize:vertical}
.contact-form button{justify-self:start;font-family:var(--mono);font-size:.85rem;color:var(--paper);background:var(--ink);border:0;border-radius:8px;padding:.65rem 1.3rem;cursor:pointer}
.contact-form button:disabled{opacity:.55;cursor:default}
.contact-form .trap{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.contact-status{font-family:var(--mono);font-size:.8rem;color:var(--muted);margin:0;min-height:1.2em}
:focus-visible{outline:2px solid var(--drifting);outline-offset:2px}
"""

FONTS = ('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800'
         '&family=IBM+Plex+Mono:wght@400;500&family=Literata:opsz,wght@7..72,400..700&family=Comic+Neue:wght@700&display=swap')


# Where the contact form on the Next page sends its leads: the n8n essay-lead webhook.
# The form asks for a name, an email and an open message, "How are you doing?" (Alex, 17 October); only
# the email is required. It posts name, email and message, plus the UTM fields and page_url, as urlencoded POST.
# The webhook took name and email before; the message field is new, so the workflow has to pass it on.
CONTACT_ENDPOINT = 'https://n8n.giving-school.eu/webhook/essay-lead'

# Runs on every page, so UTM values from the page a reader lands on still reach the form on the Next page.
UTM_JS = """
(function () {
  try {
    var q = new URLSearchParams(location.search), s = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) { if (q.get(k)) s[k] = q.get(k); });
    if (Object.keys(s).length) sessionStorage.setItem('essay_utm', JSON.stringify(s));
  } catch (e) {}
})();
"""

CONTACT_JS = """
document.querySelectorAll('.contact-form').forEach(function (f) {
  var el = function (n) { return f.elements.namedItem(n); };
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var s = f.querySelector('.contact-status'), btn = f.querySelector('button');
    if (el('website').value) { s.textContent = 'Thank you.'; return; }
    var d = new URLSearchParams(), v = el('email').value.trim();
    if (!v) { s.textContent = 'Add your email, then send.'; return; }
    d.set('email', v);
    ['name', 'message'].forEach(function (k) { var x = el(k).value.trim(); if (x) d.set(k, x); });
    var utm = {};
    try { utm = JSON.parse(sessionStorage.getItem('essay_utm') || '{}'); } catch (x) {}
    Object.keys(utm).forEach(function (k) { if (/^utm_/.test(k) && utm[k]) d.set(k, utm[k]); });
    d.set('page_url', location.href);
    btn.disabled = true; s.textContent = 'Sending\u2026';
    fetch(f.dataset.endpoint, { method: 'POST', body: d })
      .then(function (r) { if (!r.ok) throw new Error(r.status); f.reset(); s.textContent = 'Thank you. I got it, and I\u2019ll try to keep you updated.'; })
      .catch(function () { s.textContent = 'That didn\u2019t go through. Please try again in a minute.'; })
      .finally(function () { btn.disabled = false; });
  });
});
"""


def contact_html(intro=''):
    return ('<section class="contact" aria-label="Get in touch">'
            + (f'<p>{smart(intro)}</p>' if intro else '') +
            f'<form class="contact-form" data-endpoint="{html.escape(CONTACT_ENDPOINT)}">'
            '<label>Your name<input name="name" autocomplete="name" maxlength="120"></label>'
            '<label>Your email<input name="email" type="email" autocomplete="email" maxlength="200"></label>'
            '<label>How are you doing?<span class="hint">Please share anything you feel.</span>'
            '<textarea name="message" rows="5" maxlength="2000"></textarea></label>'
            '<label class="trap" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>'
            '<button type="submit">Send</button>'
            '<p class="contact-status" role="status" aria-live="polite"></p>'
            '</form></section>'
            f'<script>{CONTACT_JS}</script>')


# Every fold says what kind of thing is inside (Josh and Ruth joint read, 2026-10-18, design 2):
# an icon, a colored kind line with the count, the title, and the first entry fading out.
# Folds are from the traditions unless listed here by title.
FOLD_KINDS = {
    'What the studies say': 'study',
    'What the studies say about sticking with it': 'study',
    'But why would it do that?': 'look',
    'A post-mortem, the way we do it at work': 'look',
    "What if I'm not sure?": 'life',
    'My teacher and I': 'story',
}
KIND_LABEL = {'trad': ('From the traditions', 'passage', 'passages'), 'study': ('From the studies', 'study', 'studies'),
              'look': ('A closer look', None, None), 'life': ("From people's lives", 'example', 'examples'),
              'story': ('My own story', None, None)}
KIND_ICON = {
    'trad': '<path d="M3 5.5c3-1.2 6-1 9 1v13c-3-2-6-2.2-9-1z"/><path d="M21 5.5c-3-1.2-6-1-9 1v13c3-2 6-2.2 9-1z"/>',
    'study': '<path d="M9 3h6"/><path d="M10 3v6l-5.5 9.5A1.6 1.6 0 0 0 5.9 21h12.2a1.6 1.6 0 0 0 1.4-2.5L14 9V3"/><path d="M7.5 15h9"/>',
    'look': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
    'life': '<circle cx="8" cy="7" r="3"/><circle cx="16.5" cy="8.5" r="2.5"/><path d="M2.5 20c.6-4 2.8-6.5 5.5-6.5s4.9 2.5 5.5 6.5"/><path d="M14 14.2c.8-.5 1.6-.7 2.5-.7 2.4 0 4.2 2.2 4.8 5.5"/>',
    'story': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
}
FOLD_KINDS_SEEN = set()


def fold_html(title, block, lis):
    kind = FOLD_KINDS.get(title, 'trad')
    FOLD_KINDS_SEEN.add(title)
    entries = [l[2:] for l in block.split('\n') if l.startswith('* ') and not l.endswith(':')]
    label, one, many = KIND_LABEL[kind]
    if one:
        label += f' · {len(entries)} {one if len(entries) == 1 else many}'
    first = html.unescape(re.sub(r'<[^>]+>', '', smart(entries[0]))).strip() if entries else ''
    if len(first) > 120:
        first = first[:120].rsplit(' ', 1)[0] + '…'
    icon = (f'<svg class="ki" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{KIND_ICON[kind]}</svg>')
    return (f'<details class="say-fold k-{kind}"><summary>{icon}<span class="kt"><span class="kk">{html.escape(label)}</span>'
            f'<span class="tt">{smart(title)}</span><span class="tz" aria-hidden="true">{html.escape(first)}</span></span>'
            f'<span class="pm" aria-hidden="true"></span></summary><div class="kb"><ul class="say">{lis}</ul></div></details>')


def convert(md, R):
    blocks = [b for b in re.split(r'\n\s*\n', md.strip()) if b.strip()]
    out = []
    toc = []
    in_sources = False
    fold_title = None
    for b in blocks:
        b = b.strip('\n')
        if b.startswith('# '):
            continue
        if b.startswith('## '):
            t = b[3:].strip()
            in_sources = (t == 'Sources')
            toc.append((slug(t), t))
            out.append(f'<h2 id="{slug(t)}">{smart(t)}</h2>')
            continue
        if b.startswith('### '):
            t = b[4:].strip()
            room = {'Default': 'default', 'Driven': 'driven', 'Drifting': 'drifting', 'High agency': 'high'}.get(t, 'default')
            out.append(f'<h3 class="room {room}"><span class="dot"></span>{smart(t)}</h3>')
            continue
        if b.startswith('  ') and out and out[-1].endswith('</ul></div></details>'):  # an indented paragraph closes the fold above it
            out[-1] = out[-1][:-len('</div></details>')] + f'<p class="say-close">{smart(b.strip())}</p></div></details>'
            continue
        if fold_title and not b.startswith('* '):  # a heading with no list under it stays a heading
            out.append(f'<h4>{smart(fold_title)}</h4>')
            fold_title = None
        if b.startswith('#### '):
            fold_title = b[5:].strip()  # every #### heading folds the list under it
            continue
        if b.startswith('* '):
            def li(l):
                t = l[2:]
                if t.endswith(':'):  # a bullet ending in a colon labels the ones after it
                    return f'<li class="grp">{smart(t)}</li>'
                rule = next((v for k, v in R.items() if 'li_after' in v and t.startswith(k)), None)  # li_after puts a figure inside the entry
                return f'<li>{smart(t)}{rule["li_after"] if rule else ""}</li>'
            lis = ''.join(li(l) for l in b.split('\n') if l.startswith('* '))
            if fold_title:
                out.append(fold_html(fold_title, b, lis))
                fold_title = None
            else:
                out.append(f'<ul class="say">{lis}</ul>')
            continue
        if b.startswith('- '):
            lis = ''.join(f'<li>{smart(l[2:])}</li>' for l in b.split('\n') if l.startswith('- '))
            out.append(f'<ul class="sources">{lis}</ul>')
            continue
        if in_sources and len(b) < 60:
            out.append(f'<h4>{smart(b)}</h4>')
            continue
        if b.startswith('[ALEX'):
            out.append(f'<p class="slot">{smart(b)}</p>')
            continue
        if b.startswith('[CONTACT:'):
            if CONTACT_ENDPOINT:  # no endpoint yet: leave the form off the page
                out.append(contact_html(b[len('[CONTACT:'):].rstrip(']').strip()))
            continue
        para = f'<p>{smart(b)}</p>'
        rule = next((v for k, v in R.items() if b.startswith(k)), None)
        if rule:
            if 'who' in rule:
                figs = ''.join(who(k, n, r) for k, n, r in rule['who'])
                out.append(item(figs, para))
                if rule.get('after'):
                    out.append(rule['after'])
            else:
                if rule.get('before'):
                    out.append(rule['before'])
                out.append(para)
                if rule.get('after'):
                    out.append(rule['after'])
        else:
            out.append(para)
    starts = [b.strip() for b in blocks] + [l[2:] for b in blocks for l in b.split('\n') if l.startswith('* ')]
    unused = [k for k in R if not any(s.startswith(k) for s in starts)]
    if unused:
        print('  note: placement rules that matched no paragraph:', *unused, sep='\n    ')
    return out, toc


NAMES = ['Intro', 'Rational', 'Spiritual', 'Practical', 'Contact']  # the chapters, in order; Contact is the page after the essay (contact.md)
HEADS = ['Before you start', 'Rational', 'Spiritual', 'Practical', 'Stay in contact']
NUMS = ['Part zero', 'Part one', 'Part two', 'Part three', 'After the book']
# The book's name in the sidebar (Alex, 2026-10-29).
BOOK_TITLE = 'Rational, Spiritual, Practical'
BOOK_SUB = 'A modern take on the path from micro to macro'  # Alex, 2026-10-29
BOOK_BY = 'by Alex'
# Where each chapter lives on the website. --preview links the built files instead, for a preview copy.
SITE_URLS = ['/intro', '/rational', '/spiritual', '/practical', '/contact']
FILE_URLS = ['part-0-intro.html', 'part-1-rational.html', 'part-2-spiritual.html', 'part-3-practical.html', 'contact.html']
URLS = SITE_URLS
# The PDF and the EPUB, built by tools/build_book.py into essay/book/ and served from the public repo,
# so the download works without a change on the web server.
BOOK_FILES = 'https://raw.githubusercontent.com/AxelPotato/magnum-opus/main/essay/book/rational-spiritual-practical'
WPM = 230  # reading speed for the minutes shown under each chapter title


def part_md(n):
    return open(os.path.join(HERE, PARTS[n]['md']), encoding='utf-8').read()


def reading_words(md):
    body = re.split(r'\n## Sources\b', md)[0]
    body = re.sub(r'^#.*$', '', body, flags=re.M)
    return len(re.findall(r"[A-Za-z0-9’']+", body))


def heads_of(md):
    return [(slug(t), t) for t in re.findall(r'^## (.+?)\s*$', md, flags=re.M)]


def hero_html(part, words=0):
    backup = part == '2a'
    if backup:
        part = 2
    lede = {
        0: 'What each part is for, who is talking, and who taught me.',
        1: 'Two directions, four rooms, and a map that turns out to be bigger than it looks.',
        2: 'Two ways of reading a life, one assumption that separates them, and what follows from it in the world\'s religions.',
        3: 'How this is done today, by people with jobs, families and not much spare time.',
        4: '',  # the contact page opens straight on its own sentence
    }[part]
    kicker = NUMS[part]
    if backup:
        lede = 'What the middle of the chart is, what lies past the edge of it, and why a rational person might want to find out.'
        kicker = 'Backup: an earlier version of part two'
    mins = round(words / WPM / 5) * 5 if words > 1500 else (max(1, round(words / WPM)) if words else 0)
    meta = f'<p class="meta">About {mins} minutes of reading</p>' if part in (0, 1, 2, 3) and mins else ''
    return ('<header class="hero"><div class="hero-in">'
            f'<p class="kicker">{kicker}</p>'
            f'<h1>{HEADS[part]}</h1>'
            + (f'<p class="lede">{lede}</p>' if lede else '') + meta +
            '<div class="orn" aria-hidden="true"><span></span><i></i><span></span></div>'
            '</div></header>')


def book_nav(part, toc):
    """The whole book in the sidebar: every chapter, the one being read open to its sections."""
    lis = []
    for n, name in enumerate(NAMES):
        on = n == part
        secs = toc if on else heads_of(part_md(n))
        base = '' if on else URLS[n]
        sec_html = ''.join(f'<li><a href="{base}#{s}">{smart(t)}</a></li>' for s, t in secs)
        head = (f'<a class="ch-a" href="{URLS[n]}"' + (' aria-current="page"' if on else '') + '>'
                f'<span class="ch-n">{NUMS[n] if n < 4 else "After"}</span><span class="ch-t">{HEADS[n]}</span></a>')
        if not secs:
            lis.append(f'<li class="ch{" on" if on else ""}">{head}</li>')
        elif on:
            lis.append(f'<li class="ch on">{head}<ol class="secs">{sec_html}</ol><span class="ch-bar" aria-hidden="true"><i></i></span></li>')
        else:
            lis.append(f'<li class="ch"><details><summary aria-label="Show the sections of {HEADS[n]}">{head}<span class="chev" aria-hidden="true"></span></summary>'
                       f'<ol class="secs">{sec_html}</ol></details></li>')
    return ('<nav class="book" id="toc" aria-label="The book">'
            f'<a class="bk" href="{URLS[0]}"><span class="bk-t">{BOOK_TITLE}</span><span class="bk-sub">{BOOK_SUB}</span><span class="bk-by">{BOOK_BY}</span></a>'
            f'<ol class="chapters">{"".join(lis)}</ol>'
            '<div class="downloads"><p>Download the book</p>'
            f'<a href="{BOOK_FILES}.pdf" download>PDF</a><a href="{BOOK_FILES}.epub" download>EPUB</a>'
            '<span>EPUB works on Kindle (through Send to Kindle), Kobo and Apple Books.</span></div></nav>')


def turn_html(part):
    """Where the chapter ends: the previous and the next chapter, like turning a page."""
    out = []
    if part > 0:
        out.append(f'<a class="prev" href="{URLS[part - 1]}"><span>Previous</span><b>{NUMS[part - 1]}: {HEADS[part - 1]}</b></a>')
    if part < 4:
        nxt = f'{NUMS[part + 1]}: {HEADS[part + 1]}' if part < 3 else HEADS[4]
        out.append(f'<a class="next" href="{URLS[part + 1]}"><span>Next</span><b>{nxt}</b></a>')
    return '<nav class="turn" aria-label="Chapters">' + ''.join(out) + '</nav>'


def cast_html():
    cast_people = [('squidward', 'default', 'Squidward'), ('costanza', 'default', 'George Costanza'), ('hank', 'default', 'Hank Hill'), ('jim', 'default', 'Jim Halpert'),
                   ('pam', 'default', 'Pam Beesly'), ('carrey', 'driven', 'Jim Carrey'), ('phelps', 'driven', 'Michael Phelps'), ('biles', 'driven', 'Simone Biles'),
                   ('dude', 'drifting', 'The Dude'), ('phoebe', 'drifting', 'Phoebe Buffay'), ('welwood', 'drifting', 'John Welwood'), ('malala', 'high', 'Malala Yousafzai'),
                   ('aurelius', 'high', 'Marcus Aurelius'), ('parks', 'high', 'Rosa Parks')]
    return ('<div class="cast" role="group" aria-label="The cast of this part">' + ''.join(
        f'<img class="{r}" src="{uri(k, 120)}" alt="{n}" title="{n}" width="54" height="54">' for k, r, n in cast_people) + '</div><p class="cast-cap">Who shows up in this part</p>')


PART1_FOOT = ('Character and portrait images are used as illustration in a personal draft. Check image rights before this goes public. '
              'Free-licensed portraits from Wikimedia Commons: Henry David Thoreau (public domain, Benjamin D. Maxham), Viktor Frankl (CC BY-SA 3.0 DE, Franz Vesely), '
              'Tal Ben-Shahar (CC0), Rosa Parks (public domain).')
PART2_FOOT = 'A draft. The pictures in this part are drawn for it.'

PART0_FOOT = 'A draft.'
PART3_FOOT = 'A draft. The drawings in this part are drawn for it, and the two photos are of me.'
NEXT_FOOT = 'A draft.'

# The book's contents: a left sidebar on wide screens, a drawer behind a top bar on narrow ones.
# Everything is scoped to body.has-toc, which only the standalone pages get (not the fragment).
TOC_CSS = r"""
.topbar,.toc-scrim,.progress{display:none}
body.has-toc .progress{display:block;position:fixed;left:0;right:0;top:0;height:3px;z-index:60;pointer-events:none}
body.has-toc .progress i{display:block;height:100%;width:100%;background:var(--accent);transform-origin:0 50%;transform:scaleX(0)}
body.has-toc .topbar{display:flex;align-items:center;gap:.75rem;position:fixed;top:0;left:0;right:0;z-index:40;height:3.25rem;padding:0 .75rem;background:color-mix(in srgb,var(--paper) 92%,transparent);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-bottom:1px solid var(--rule)}
.toc-btn{display:flex;align-items:center;justify-content:center;flex:none;width:2.4rem;height:2.4rem;padding:0;border:1px solid var(--rule);border-radius:8px;background:var(--card);color:var(--ink);cursor:pointer}
.toc-btn:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
.topbar .tb-t{min-width:0;font-family:var(--head);font-size:1rem;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.topbar .tb-t span{color:var(--muted);font-family:var(--mono);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;margin-right:.5rem}
body.has-toc .book{position:fixed;left:0;top:0;bottom:0;width:min(20rem,86vw);margin:0;padding:1.75rem 1rem 2.5rem 1.25rem;overflow-y:auto;overscroll-behavior:contain;border-right:1px solid var(--rule);background:var(--side);z-index:50;transform:translateX(-100%);visibility:hidden;transition:transform .22s ease,visibility 0s .22s;scrollbar-width:thin}
body.has-toc.toc-open .book{transform:none;visibility:visible;transition:transform .22s ease;box-shadow:0 0 40px rgba(0,0,0,.18)}
body.has-toc.toc-open .toc-scrim{display:block;position:fixed;inset:0;z-index:45;background:rgba(20,16,10,.42)}
.book a{text-decoration:none;color:inherit}
.book .bk{display:block;padding:0 .5rem 1.25rem;margin:0 0 1rem;border-bottom:1px solid var(--rule)}
.book .bk-t{display:block;font-family:var(--head);font-weight:600;font-size:1.3rem;line-height:1.15;letter-spacing:-.01em;color:var(--ink)}
.book .bk-sub{display:block;margin-top:.4rem;font-family:var(--head);font-style:italic;font-size:.95rem;line-height:1.35;color:var(--ink)}
.book .bk-by{display:block;margin-top:.45rem;font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.book ol{list-style:none;margin:0;padding:0}
.book .ch{position:relative;margin:0 0 .25rem}
.book details>summary{list-style:none;display:flex;align-items:center;cursor:pointer}
.book details>summary::-webkit-details-marker{display:none}
.book .ch-a{display:flex;flex-direction:column;flex:1;min-width:0;padding:.55rem .5rem;border-radius:8px}
.book .ch-a:hover{background:var(--hover)}
.book .ch-n{font-family:var(--mono);font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.book .ch-t{font-family:var(--head);font-size:1.08rem;line-height:1.25;color:var(--ink)}
.book .ch.on>.ch-a{background:var(--hover)}
.book .ch.on>.ch-a .ch-t{font-weight:600}
.book .ch.on>.ch-a .ch-n{color:var(--accent)}
.book .chev{flex:none;width:1.9rem;height:1.9rem;border-radius:6px;display:grid;place-items:center;color:var(--muted)}
.book .chev::before{content:"";width:.42rem;height:.42rem;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(-45deg);transition:transform .15s}
.book details[open] .chev::before{transform:rotate(45deg)}
.book summary:hover .chev{color:var(--ink);background:var(--hover)}
.book .secs{margin:.2rem 0 .7rem .5rem;padding-left:.75rem;border-left:1px solid var(--rule)}
.book .secs a{display:block;padding:.28rem .5rem;margin-left:-1px;border-left:2px solid transparent;font-family:var(--body);font-size:.88rem;line-height:1.35;color:var(--muted)}
.book .secs a:hover{color:var(--ink)}
.book .secs a.on{color:var(--ink);border-left-color:var(--accent)}
.book .ch-bar{display:block;height:2px;margin:-.3rem .5rem .8rem 1.25rem;background:var(--rule);border-radius:2px;overflow:hidden}
.book .ch-bar i{display:block;height:100%;width:100%;background:var(--accent);transform-origin:0 50%;transform:scaleX(0)}
.book .downloads{margin:1.4rem .5rem 0;padding-top:1.1rem;border-top:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:.5rem}
.book .downloads p{flex-basis:100%;margin:0 0 .1rem;font-family:var(--mono);font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.book .downloads a{font-family:var(--mono);font-size:.8rem;padding:.4rem .85rem;border:1px solid var(--ink);border-radius:999px;color:var(--ink)}
.book .downloads a:hover{background:var(--ink);color:var(--paper)}
.book .downloads span{flex-basis:100%;font-size:.8rem;line-height:1.4;color:var(--muted);margin-top:.2rem}
.book :focus-visible{outline:2px solid var(--ink);outline-offset:2px;border-radius:6px}
body.has-toc .hero{padding-top:5.5rem}
@media (min-width:72rem){
  body.has-toc{padding-left:18rem}
  body.has-toc .book{width:18rem;transform:none;visibility:visible;transition:none;box-shadow:none}
  body.has-toc .topbar,body.has-toc.toc-open .toc-scrim{display:none}
  body.has-toc .hero{padding-top:clamp(3rem,9vh,6rem)}
  body.has-toc .fig:not(.plain):not(.photo){width:min(54rem,calc(100vw - 22rem))}
}
@media print{.book,.topbar,.progress,.toc-scrim,.turn{display:none!important}body.has-toc{padding-left:0}}
"""

TOC_JS = r"""
(function () {
  var b = document.body, btn = document.querySelector('.toc-btn'), nav = document.getElementById('toc');
  if (!btn || !nav) return;
  function set(o) { b.classList.toggle('toc-open', o); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); }
  btn.addEventListener('click', function () { set(!b.classList.contains('toc-open')); });
  document.querySelector('.toc-scrim').addEventListener('click', function () { set(false); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  var links = [].slice.call(nav.querySelectorAll('.ch.on .secs a')), last = -2;
  var heads = links.map(function (a) { return document.getElementById(a.getAttribute('href').split('#')[1]); });
  var bars = [].slice.call(document.querySelectorAll('.progress i,.ch-bar i')), main = document.querySelector('main');
  function spy() {
    var y = window.innerHeight * 0.25, cur = -1;
    if (main) {
      var r = main.getBoundingClientRect(), f = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - window.innerHeight)));
      bars.forEach(function (i) { i.style.transform = 'scaleX(' + f + ')'; });
    }
    heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top <= y) cur = i; });
    if (cur === last) return;
    last = cur;
    links.forEach(function (a, i) { a.classList.toggle('on', i === cur); if (i === cur) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current'); });
    if (cur >= 0) { var a = links[cur], t = a.getBoundingClientRect().top - nav.getBoundingClientRect().top; if (t < 60 || t > nav.clientHeight - 60) nav.scrollTop += t - nav.clientHeight / 3; }
  }
  window.addEventListener('scroll', spy, { passive: true });
  window.addEventListener('resize', spy);
  spy();
})();
"""

PARTS = {
    0: dict(md='part-0-intro.md', out='part-0-intro.html', title='Part Zero: Before you start', rules=lambda: rules0(), cast=False, css_extra=PART0_CSS, foot=PART0_FOOT),
    1: dict(md='part-1-rational.md', out='part-1-rational.html', title='Part One: Rational', rules=rules1, cast=False, css_extra='', foot=PART1_FOOT),
    2: dict(md='part-2-spiritual.md', out='part-2-spiritual.html', title='Part Two: Spiritual', rules=lambda: rules2(), cast=False, css_extra=F3.CSS_EXTRA + F4.CSS_EXTRA + F5.CSS_EXTRA + F6.CSS_EXTRA, foot=PART2_FOOT),
    3: dict(md='part-3-practical.md', out='part-3-practical.html', title='Part Three: Practical', rules=rules3, cast=False, css_extra=F3.CSS_EXTRA + F4.CSS_EXTRA + F5.CSS_EXTRA + PART0_CSS, foot=PART3_FOOT),
    4: dict(md='contact.md', out='contact.html', title='Stay in contact', rules=lambda: {}, cast=False, css_extra='', foot=NEXT_FOOT),
    # kept for reference, not part of the default build: python build_html.py --part 2a
    '2a': dict(md='backup/part-2-variant-a-psychological.md', out='backup/part-2-variant-a-psychological.html', title='Part Two, backup: Spiritual', rules=lambda: rules2a(),
               cast=False, css_extra=F3.CSS_EXTRA, foot=PART2_FOOT + ' This is the first version of part two, kept as a backup.', fixed_ver='1.0.0', backup=True),
}


def page(part, fragment=False):
    cfg = PARTS[part]
    md = open(os.path.join(HERE, cfg['md']), encoding='utf-8').read()
    ver = cfg.get('fixed_ver') or open(os.path.join(HERE, '..', 'VERSION'), encoding='utf-8').read().strip()
    body, toc = convert(md, cfg['rules']())
    book = part in range(5) and not fragment  # the backup page keeps the old plain layout
    first = next((i for i, x in enumerate(body) if x.startswith('<p>')), None)
    if book and first is not None and part != 4:  # a drop cap on the chapter's first paragraph
        body[first] = '<p class="first">' + body[first][3:]
    if book:
        nav = book_nav(part, toc)
    elif toc:
        nav = '<nav class="toc" aria-label="In this part">' + ' '.join(f'<a href="#{s}">{smart(t)}</a>' for s, t in toc) + '</nav>'
    else:
        nav = ''
    main = ('<main><div class="col">' + (nav if not book else '') + (cast_html() if cfg['cast'] else '')
            + '\n'.join(body) + '</div>' + (turn_html(part) if book else '') +
            f'<footer>Version {ver}. Built from {cfg["md"]}. ' + cfg['foot'] + '</footer></main>')
    head = (f'<title>{cfg["title"]}</title>'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="version" content="{ver}">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="{FONTS}"><style>{CSS}{TOC_CSS}{cfg["css_extra"]}</style>'
            f'<script>{UTM_JS}</script>')
    hero = hero_html(part, reading_words(md) if part != '2a' else 0)
    if fragment:
        return head + hero + main
    if not book:
        return ('<!doctype html><html lang="en"><head><meta charset="utf-8">' + head + '</head><body>' + hero + main + '</body></html>')
    bar = ('<div class="progress" aria-hidden="true"><i></i></div>'
           '<div class="topbar"><button class="toc-btn" type="button" aria-label="Contents" aria-expanded="false" aria-controls="toc">'
           '<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg></button>'
           f'<p class="tb-t"><span>{NUMS[part]}</span>{HEADS[part]}</p></div>'
           '<div class="toc-scrim"></div>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">' + head + '</head><body class="has-toc">' + bar + nav + hero + main
            + f'<script>{TOC_JS}</script></body></html>')


if __name__ == '__main__':
    args = sys.argv[1:]
    frag = '--fragment' in args
    if '--preview' in args:  # link the chapters by file name, for a preview copy outside the website
        URLS = FILE_URLS
    only = args[args.index('--part') + 1] if '--part' in args else None
    for n, cfg in PARTS.items():
        if only and str(n) != only:
            continue
        if cfg.get('backup') and not only:
            continue
        if not os.path.exists(os.path.join(HERE, cfg['md'])):
            continue
        out = os.path.join(HERE, cfg['out'])
        if frag:
            out = out.replace('.html', '.fragment.html')
        text = page(n, frag)
        open(out, 'w', encoding='utf-8').write(text)
        print(out, round(len(text) / 1024), 'KB')
    if not only:
        stale = [k for k in FOLD_KINDS if k not in FOLD_KINDS_SEEN]
        if stale:
            print('  note: fold kinds that matched no fold title:', *stale, sep='\n    ')
