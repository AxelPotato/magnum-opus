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
    if key == 'scooby':
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
        mini_square(50, 50, 'high soft', 'The middle', '2,500'),
        mini_square(80, 80, 'high mid', 'Further in', '6,400'),
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
        'If DO and BE sound like a Sinatra': dict(after=figure(
            f'<img class="scooby" src="{uri("scooby")}" alt="Scooby-Doo" width="800" height="450" loading="lazy">',
            'BE: where are you? DO: there is a man in a mask.', 'photo')),
        'Draw them as a cross.': dict(after=figure(svg_cross(), 'The cross. DO runs left to right, BE runs bottom to top. Each room with the people who will show up in it.')),
        'Squidward is the most extreme': dict(who=[('squidward', 'Squidward', 'default')]),
        'George Costanza is the exit story': dict(who=[('costanza', 'George Costanza', 'default')]),
        'Hank Hill is that corner': dict(before=row([('hank', 'Hank Hill', 'default'), ('jim', 'Jim Halpert', 'default'), ('pam', 'Pam Beesly', 'default')])),
        'Jim Carrey is one answer': dict(who=[('carrey', 'Jim Carrey', 'driven')]),
        'Michael Phelps is the same story': dict(who=[('phelps', 'Michael Phelps', 'driven')]),
        'Simone Biles is the most decorated': dict(who=[('biles', 'Simone Biles', 'driven')]),
        'The only popular example I could find': dict(who=[('dude', 'The Dude', 'drifting')]),
        'Phoebe from Friends': dict(who=[('phoebe', 'Phoebe Buffay', 'drifting')]),
        'There is a name for those escape moves': dict(who=[('welwood', 'John Welwood', 'neutral')]),
        'Malala Yousafzai kept going': dict(who=[('malala', 'Malala Yousafzai', 'high')]),
        'Marcus Aurelius ran the Roman Empire': dict(who=[('aurelius', 'Marcus Aurelius', 'high')]),
        'Rosa Parks is a good one': dict(who=[('parks', 'Rosa Parks', 'high')]),
        'Somewhere around the middle, 50 and 50': dict(after=figure(squares(), 'The same square, six ways. Width is DO, height is BE, the shaded part is the area a person takes up.', 'plain')),
        'On the line, what you\'re free to want': dict(after=figure(svg_line(), 'The line of harmony. Position along it says how far you have come. Distance from it says how much is leaking.')),
        'Learning to walk on two legs': dict(after=figure(svg_swing(), 'A swing that narrows, then the climb, which stays wavy until the peak. Illustration, not data.')),
        'Zoom out by ten': dict(after=figure(svg_zoom(), 'Zoom out by ten. The whole square we have been using is the small box in the corner.')),
        'Picture the steering wheel of your life.': dict(after=figure(F.fig_wheel(), 'Hands on the wheel, or in the back seat.')),
        'Asking is a quiet one': dict(after=figure(F.icons_html(), 'Five quiet kinds of DO.', 'plain')),
        'It matters even if you couldn': dict(after=figure(F.fig_shelf(), 'The tax on seeing solutions: most of the shelf is ruled out before you look.')),
        'Here is the connection to being here.': dict(after=figure(F.fig_attention(), 'Where your attention is, as opposed to where your body is.')),
        'The turbulence comes from walking on two legs.': dict(after=figure(F.fig_legs(), 'Three ways to move. The DO leg is vermilion, the BE leg is blue.')),
        'Here is why the turbulence is worth it': dict(after=figure(F.fig_loop(), 'The two legs feed each other.')),
        'A quick way to find your own examples': dict(who=[('bezos', 'Jeff Bezos', 'neutral')], after=figure(F.fig_jail(), 'The jail-cell test.')),
        'Say each line runs from 0 to 100.': dict(after=figure(F.fig_bars(), 'Effectiveness is roughly BE times DO. Do not quote me.')),
        'Start with the physiology.': dict(after=figure(F.fig_anokhin(), 'Anokhin\'s functional system, simplified: a goal is a model of the result, and the result is compared with it.')),
        'Viktor Frankl, a psychiatrist': dict(who=[('frankl', 'Viktor Frankl', 'neutral')]),
        'A sense of purpose in general points the same way.': dict(after=figure(F.fig_studies(), 'Left: a randomized field experiment. Right: a review of ten long-term studies, which shows an association, not a cause. Read both as a direction.')),
        'Picture someone who freezes': dict(after=figure(F.fig_scales(), 'The fear is a vote. A bigger reason is a bigger vote.')),
        'A lot of the tension is also made of self-monitoring': dict(after=figure(F.fig_spot(), 'The spotlight effect: we overestimate how much others notice us.')),
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
        'Almost everybody has visited.': dict(after=figure(F.icons_flow_html(), 'Different rooms, same visit.', 'plain')),
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


def rules2():
    return {
        'The second view sits at the other extreme': dict(after=figure(F4.fig_views(), 'Two assumptions at opposite ends. Neither can be observed from outside, since the observing is done by the same mind.')),
        'Under the axiom, you and I are programs.': dict(after=figure(F4.fig_cpu(), 'Far apart on the screen, side by side in the machine. The distance is a property of the drawing.')),
        'It also turns out that the wall is built from soft material.': dict(after=figure(F3.fig_rubber(), 'The rubber hand illusion. The felt border of the body is something the brain works out, and it can be moved.')),
        'The body keeps it in place.': dict(after=figure(F3.fig_fist(), 'The same person, tensed and then released.')),
        'And if the run continues': dict(after=figure(F4.fig_lives(), 'If the process is a return, and most people do not finish it in one life, it has to run longer than one life.')),
        'If we are one, there is nobody else.': dict(after=figure(F4.fig_fingers(), 'Karma, with the courtroom taken out.')),
        'Every room on the chart is a separate program': dict(after=figure(F3.fig_rooms(), 'Four rooms, one assumption underneath.')),
        "I've found one picture that carries the whole scale": dict(after=figure(F4.fig_arrow(), 'The arrow of consciousness as speed and freedom of movement. Gravity is the pull of the position you started from.')),
        'The top right corner of the small square is escape velocity': dict(after=figure(F4.fig_escape(), 'From orbit to escape is a small change in speed and a total change in outcome.')),
    }


# ---------------------------------------------------------------- build
CSS = r"""
:root{
  --paper:#F4F6FA; --ink:#131C33; --muted:#5A6480; --rule:#D5DBE8; --grid:#E4E9F2; --card:#FFFFFF;
  --default:#6B7A99; --driven:#D2502F; --drifting:#4A66D6; --high:#0C8A6A;
  --display:'Bricolage Grotesque','Segoe UI',system-ui,sans-serif;
  --body:'Literata',Georgia,'Times New Roman',serif;
  --mono:'IBM Plex Mono',ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#0E1424; --ink:#E7EBF5; --muted:#9AA5C0; --rule:#27314D; --grid:#161E35; --card:#151D33;
  --default:#8E9BBA; --driven:#F0724F; --drifting:#7B93F0; --high:#31C79F; color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#0E1424; --ink:#E7EBF5; --muted:#9AA5C0; --rule:#27314D; --grid:#161E35; --card:#151D33;
  --default:#8E9BBA; --driven:#F0724F; --drifting:#7B93F0; --high:#31C79F; color-scheme:dark}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:1.125rem;line-height:1.68;overflow-x:clip}
.hero{position:relative;padding:clamp(2.5rem,7vw,5rem) 1rem 2rem}
.hero::before{content:"";position:absolute;inset:0;z-index:0;
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:32px 32px;
  -webkit-mask-image:linear-gradient(#000 70%,transparent);mask-image:linear-gradient(#000 70%,transparent)}
.hero-in{position:relative;z-index:1;max-width:40rem;margin:0 auto}
.kicker{font-family:var(--mono);font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 .8rem}
h1{font-family:var(--display);font-weight:800;font-size:clamp(3.4rem,13vw,6.2rem);line-height:.95;letter-spacing:-.03em;margin:0;text-wrap:balance}
.lede{font-size:1.3rem;line-height:1.45;margin:1.2rem 0 1.4rem;max-width:32rem;color:var(--ink)}
.parts{display:flex;flex-wrap:wrap;gap:.5rem;margin:0;padding:0;list-style:none;font-family:var(--mono);font-size:.82rem}
.parts li{padding:.3rem .7rem;border:1px solid var(--rule);border-radius:999px;color:var(--muted);background:var(--paper)}
.parts li.now{border-color:var(--ink);color:var(--ink);font-weight:500}
main{padding:0 1rem 4rem}
.col{max-width:40rem;margin:0 auto}
.toc{font-family:var(--mono);font-size:.82rem;line-height:1.9;margin:0 0 2.5rem;padding:1rem 0;border-block:1px solid var(--rule)}
.toc a{color:var(--muted);text-decoration:none;margin-right:1rem;white-space:nowrap}
.toc a:hover{color:var(--ink);text-decoration:underline}
h2{font-family:var(--display);font-weight:800;font-size:clamp(1.9rem,6vw,2.5rem);line-height:1.1;letter-spacing:-.02em;margin:3.6rem 0 1.1rem;text-wrap:balance;scroll-margin-top:1rem}
h3.room{font-family:var(--display);font-weight:700;font-size:1.55rem;margin:2.6rem 0 .9rem;display:flex;align-items:center;gap:.6rem}
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
.squares{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem 1rem;max-width:34rem;margin:0 auto}
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
.sources li{margin-bottom:.7rem;overflow-wrap:anywhere}
h4{font-family:var(--mono);font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:1.6rem 0 .8rem;font-weight:500}
footer{max-width:40rem;margin:0 auto;padding:1.5rem 0 0;border-top:1px solid var(--rule);font-family:var(--mono);font-size:.74rem;line-height:1.6;color:var(--muted)}
a{color:var(--high)}
:focus-visible{outline:2px solid var(--drifting);outline-offset:2px}
"""

FONTS = ('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800'
         '&family=IBM+Plex+Mono:wght@400;500&family=Literata:opsz,wght@7..72,400..700&family=Comic+Neue:wght@700&display=swap')


def convert(md, R):
    blocks = [b for b in re.split(r'\n\s*\n', md.strip()) if b.strip()]
    out = []
    toc = []
    in_sources = False
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
        if b.startswith('- '):
            lis = ''.join(f'<li>{smart(l[2:])}</li>' for l in b.split('\n') if l.startswith('- '))
            out.append(f'<ul class="sources">{lis}</ul>')
            continue
        if in_sources and len(b) < 60:
            out.append(f'<h4>{smart(b)}</h4>')
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
    unused = [k for k in R if not any(b.strip().startswith(k) for b in blocks)]
    if unused:
        print('  note: placement rules that matched no paragraph:', *unused, sep='\n    ')
    return out, toc


def hero_html(part):
    backup = part == '2a'
    if backup:
        part = 2
    names = ['Rational', 'Spiritual', 'Practical']
    nums = ['one', 'two', 'three']
    lede = {
        1: 'Two directions, four rooms, and a map that turns out to be bigger than it looks.',
        2: 'Two ways of reading a life, one assumption that separates them, and what follows from it in the world\'s religions.',
    }[part]
    if backup:
        lede = 'What the middle of the chart is, what lies past the edge of it, and why a rational person might want to find out.'
    lis = ''.join(f'<li class="now">{n}</li>' if i == part - 1 else f'<li>{n}</li>' for i, n in enumerate(names))
    return ('<header class="hero"><div class="hero-in">'
            f'<p class="kicker">{"Backup: an earlier version of part two" if backup else "Part " + nums[part - 1] + " of three"}</p>'
            f'<h1>{names[part - 1]}</h1>'
            f'<p class="lede">{lede}</p>'
            f'<ul class="parts">{lis}</ul>'
            '</div></header>')


def cast_html():
    cast_people = [('squidward', 'default', 'Squidward'), ('costanza', 'default', 'George Costanza'), ('hank', 'default', 'Hank Hill'), ('jim', 'default', 'Jim Halpert'),
                   ('pam', 'default', 'Pam Beesly'), ('carrey', 'driven', 'Jim Carrey'), ('phelps', 'driven', 'Michael Phelps'), ('biles', 'driven', 'Simone Biles'),
                   ('dude', 'drifting', 'The Dude'), ('phoebe', 'drifting', 'Phoebe Buffay'), ('welwood', 'drifting', 'John Welwood'), ('malala', 'high', 'Malala Yousafzai'),
                   ('aurelius', 'high', 'Marcus Aurelius'), ('parks', 'high', 'Rosa Parks')]
    return ('<div class="cast" role="group" aria-label="The cast of this part">' + ''.join(
        f'<img class="{r}" src="{uri(k, 120)}" alt="{n}" title="{n}" width="54" height="54">' for k, r, n in cast_people) + '</div><p class="cast-cap">Who shows up in this part</p>')


PART1_FOOT = ('Character and portrait images are used as illustration in a personal draft. Check image rights before this goes public. '
              'Free-licensed portraits from Wikimedia Commons: Henry David Thoreau (public domain, Benjamin D. Maxham), Viktor Frankl (CC BY-SA 3.0 DE, Franz Vesely), '
              'Tal Ben-Shahar (CC0), Jeff Bezos (public domain, US government photo), Rosa Parks (public domain).')
PART2_FOOT = 'A draft. The pictures in this part are drawn for it.'

PARTS = {
    1: dict(md='part-1-rational.md', out='part-1-rational.html', title='Part One: Rational', rules=rules1, cast=True, css_extra='', foot=PART1_FOOT),
    2: dict(md='part-2-spiritual.md', out='part-2-spiritual.html', title='Part Two: Spiritual', rules=lambda: rules2(), cast=False, css_extra=F3.CSS_EXTRA + F4.CSS_EXTRA, foot=PART2_FOOT),
    # kept for reference, not part of the default build: python build_html.py --part 2a
    '2a': dict(md='backup/part-2-variant-a-psychological.md', out='backup/part-2-variant-a-psychological.html', title='Part Two, backup: Spiritual', rules=lambda: rules2a(),
               cast=False, css_extra=F3.CSS_EXTRA, foot=PART2_FOOT + ' This is the first version of part two, kept as a backup.', fixed_ver='1.0.0', backup=True),
}


def page(part, fragment=False):
    cfg = PARTS[part]
    md = open(os.path.join(HERE, cfg['md']), encoding='utf-8').read()
    ver = cfg.get('fixed_ver') or open(os.path.join(HERE, '..', 'VERSION'), encoding='utf-8').read().strip()
    body, toc = convert(md, cfg['rules']())
    toc_html = ' '.join(f'<a href="#{s}">{smart(t)}</a>' for s, t in toc)
    main = ('<main><div class="col"><nav class="toc" aria-label="In this part">' + toc_html + '</nav>' + (cast_html() if cfg['cast'] else '')
            + '\n'.join(body) + '</div>'
            f'<footer>Version {ver}. Built from {cfg["md"]}. ' + cfg['foot'] + '</footer></main>')
    head = (f'<title>{cfg["title"]}</title>'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="version" content="{ver}">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="{FONTS}"><style>{CSS}{cfg["css_extra"]}</style>')
    if fragment:
        return head + hero_html(part) + main
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">' + head + '</head><body>' + hero_html(part) + main + '</body></html>')


if __name__ == '__main__':
    args = sys.argv[1:]
    frag = '--fragment' in args
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
