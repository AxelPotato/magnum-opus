# Regenerates every slide in slides/ plus the PDF. Edit names/lines here, run: python slides.py
from PIL import Image, ImageDraw, ImageFont, JpegImagePlugin
import math, os
FONT = "C:/Users/lelen/claude/Alex-social/Montserrat-Variable.ttf"
def F(size, w):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([w]); return f
W, H = 1920, 1080
BG = (234, 226, 212); INK = (47, 47, 47); MID = (120, 115, 105); ACC = (60, 60, 60); SW = (150, 70, 60); G = (40, 110, 80)
L, T, R, B = 300, 110, 1620, 930; cx, cy = (L + R) // 2, (T + B) // 2
ROOMS = {"default": (L + 60, B - 230, "DEFAULT", "tense · passive", "most people · fear feels like fact"),
         "driven": (cx + 60, B - 230, "DRIVEN", "tense · active", "founders, athletes · peak, then empty"),
         "drifting": (L + 60, T + 60, "DRIFTING", "released · passive", "“spiritual” people · watching their own life"),
         "whole": (cx + 60, T + 60, "HIGH AGENCY", "released · active", "outer + inner · the path, turbulent")}
ORDER = ["default", "driven", "drifting", "whole"]

def render(yaxis=False, xaxis=False, grid=False, rooms=(), corner=False, swing=False, method=False, legs=False, people=None, door=False, line=False, faces=False, title=True, stickers=()):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    def arrow(p, q, col, width=5):
        d.line([p, q], fill=col, width=width); ang = math.atan2(q[1] - p[1], q[0] - p[0]); s = 26
        a = (q[0] - s * math.cos(ang - 0.4), q[1] - s * math.sin(ang - 0.4)); b = (q[0] - s * math.cos(ang + 0.4), q[1] - s * math.sin(ang + 0.4)); d.polygon([q, a, b], fill=col)
    f = F(30, 800); f2 = F(22, 600); fl = F(22, 700)
    if title: d.text((L, 28), "RATIONAL SPIRITUALITY · the two axes of a person", font=F(34, 900), fill=INK)
    if xaxis:
        d.line([(L, B), (R, B)], fill=INK, width=6); d.polygon([(R, B), (R - 22, B - 12), (R - 22, B + 12)], fill=INK)
        d.text((R - 360, B + 28), "ACTION  →", font=f, fill=INK)
        d.text((L + 10, B + 34), "things happen to you", font=f2, fill=MID); d.text((R - 360, B + 70), "you make things happen  ·  outer agency", font=f2, fill=MID)
    if yaxis:
        d.line([(L, B), (L, T)], fill=INK, width=6); d.polygon([(L, T), (L - 12, T + 22), (L + 12, T + 22)], fill=INK)
        t = Image.new("RGBA", (700, 60), (0, 0, 0, 0)); ImageDraw.Draw(t).text((0, 0), "LETTING GO  →", font=f, fill=INK); t = t.rotate(90, expand=True); im.paste(t, (L - 90, T + 40), t)
        for lab, yy in [("braced", B - 320), ("released  ·  inner agency", T + 40)]:
            t = Image.new("RGBA", (420, 40), (0, 0, 0, 0)); ImageDraw.Draw(t).text((0, 0), lab, font=f2, fill=MID); t = t.rotate(90, expand=True); im.paste(t, (L - 60, yy), t)
    if grid:
        for i in range(0, B - T, 24): d.line([(cx, T + i), (cx, min(T + i + 12, B))], fill=MID, width=3)
        for i in range(0, R - L, 24): d.line([(L + i, cy), (min(L + i + 12, R), cy)], fill=MID, width=3)
    if door:
        rr = 120
        for a in range(0, 360, 12):
            a0, a1 = math.radians(a), math.radians(a + 7)
            d.line([(cx + rr * math.cos(a0), cy + rr * math.sin(a0)), (cx + rr * math.cos(a1), cy + rr * math.sin(a1))], fill=INK, width=4)
        if door == "label":
            d.text((cx - 470, cy + 140), "the door · most people enter the top-right here, balanced in both", font=F(22, 700), fill=INK)
    if faces:
        ff = F(30, 800); fq = F(22, 600)
        d.text((cx + 60, B - 380), "JIM CARREY · SIMONE BILES", font=ff, fill=SW)
        d.text((cx + 60, B - 342), "got everything they dreamed of. Then the crash.", font=fq, fill=SW)
        d.text((cx + 60, T + 290), "MALALA · MARCUS AURELIUS", font=ff, fill=G)
        d.text((cx + 60, T + 328), "moved the world, and did the inner work while doing it", font=fq, fill=G)
        d.text((L + 60, T + 290), "THE DUDE · PHOEBE", font=ff, fill=INK)
        d.text((L + 60, T + 328), "released, beloved · everything happens to them", font=fq, fill=MID)
        d.text((L + 60, T + 358), "Welwood named the trap, 1984: spiritual bypassing", font=fq, fill=MID)
        d.text((L + 60, B - 380), "GEORGE · PATTY & SELMA", font=ff, fill=INK)
        d.text((L + 60, B - 342), "every fear a fact · every problem is somebody else", font=fq, fill=MID)
    if line:
        # the balance line: from the door to the far corner, dotted
        x0, y0, x1, y1 = cx, cy, R - 40, T + 40; n = 70
        for i in range(0, n, 2):
            s0, s1 = i / n, (i + 1) / n
            d.line([(x0 + (x1 - x0) * s0, y0 + (y1 - y0) * s0), (x0 + (x1 - x0) * s1, y0 + (y1 - y0) * s1)], fill=INK, width=4)
        d.text((cx + 300, cy - 70), "the line · flow, in the zone, eureka, the muse, the gut", font=F(22, 700), fill=INK)
        d.text((cx + 300, cy - 40), "everyone visits · the goal is to live here", font=F(20, 600), fill=MID)
    fn = F(54, 900); fs = F(26, 500)
    for k in rooms:
        x, y, name, sub, who = ROOMS[k]
        d.text((x, y), name, font=fn, fill=INK); d.text((x, y + 66), sub, font=fs, fill=ACC); d.text((x, y + 100), who, font=fs, fill=MID)
    if swing:
        p = (cx + 330, B - 280); q = (L + 400, T + 240); arrow(p, q, SW); arrow(q, p, SW)
        d.text((cx + 360, B - 300), "the full swing: founder → island → hustle", font=fl, fill=SW)
        d.text((L + 60, T + 250), "years each way, same place, older", font=fl, fill=SW)
    if method:
        P0 = (L + 420, B - 300); P1 = (R - 70, T + 70)
        dx, dy = P1[0] - P0[0], P1[1] - P0[1]; ln = math.hypot(dx, dy); nx, ny = -dy / ln, dx / ln
        pts = []; N = 600; A = 150; k = 2.0; cyc = 3.5
        for i in range(N + 1):
            s = i / N; off = A * math.exp(-k * s) * math.sin(2 * math.pi * cyc * s)
            pts.append((P0[0] + dx * s + nx * off, P0[1] + dy * s + ny * off))
        d.line(pts, fill=G, width=7, joint="curve"); arrow(pts[-3], pts[-1], G, 7)
        d.text((L + 60, B - 390), "the method: the same swing, shrinking", font=fl, fill=G)
        d.text((cx + 230, cy + 30), "each overshoot smaller, caught earlier", font=F(20, 600), fill=G)
    if legs:
        # the two legs as the school trains them, drawn at the start of the path
        o = (L + 420, B - 300)
        arrow(o, (o[0], o[1] - 230), G, 7); arrow(o, (o[0] + 300, o[1]), G, 7)
        fb = F(24, 800); fm = F(20, 600)
        d.text((o[0] - 20, o[1] - 300), "STILLNESS  ·  inner agency", font=fb, fill=G)
        d.text((o[0] - 20, o[1] - 270), "attention inside · the brace shows, then lets go", font=fm, fill=G)
        d.text((o[0] + 40, o[1] + 14), "WORK · GIVING · PURPOSE  ·  outer agency", font=fb, fill=G)
        d.text((o[0] + 40, o[1] + 44), "real tasks with real people · the brace shows itself", font=fm, fill=G)
        d.text((cx + 60, T + 330), "every day, both legs · that is what shrinks the swing", font=F(22, 700), fill=G)
        d.text((cx + 60, T + 366), "people further along · discipline · a guided method", font=fm, fill=G)
    def damped(P0, P1, A, k, cyc, n=300):
        dx, dy = P1[0] - P0[0], P1[1] - P0[1]; ln = math.hypot(dx, dy); nx, ny = -dy / ln, dx / ln
        out = []
        for i in range(n + 1):
            s = i / n; off = A * math.exp(-k * s) * math.sin(2 * math.pi * cyc * s)
            out.append((P0[0] + dx * s + nx * off, P0[1] + dy * s + ny * off))
        return out
    def bezier(P0, C, P1, n=200):
        return [((1 - s) ** 2 * P0[0] + 2 * (1 - s) * s * C[0] + s ** 2 * P1[0], (1 - s) ** 2 * P0[1] + 2 * (1 - s) * s * C[1] + s ** 2 * P1[1]) for s in (i / n for i in range(n + 1))]
    if people == "friend-b":
        # ten years top-left → hard swing to bottom-right → ease back through the door → climb
        arrow((L + 260, T + 330), (cx + 420, B - 240), SW, 7)
        pts = bezier((cx + 420, B - 240), (cx + 380, cy - 40), (cx, cy)) + damped((cx, cy), (R - 120, T + 130), -70, 2.2, 1.5)
        d.line(pts, fill=G, width=7, joint="curve"); arrow(pts[-3], pts[-1], G, 7)
        fb = F(26, 800); fm = F(21, 600); fx = F(20, 600)
        d.text((L + 60, T + 250), "FRIEND B", font=fb, fill=INK)
        d.text((L + 60, T + 284), "ten years of ashrams · “it's all mumbo jumbo, I'm getting a job”", font=fm, fill=SW)
        d.text((cx + 60, B - 70), "business · the emptiness came back within months", font=fm, fill=SW)
        d.text((cx + 330, T + 300), "eased back through the door:", font=fx, fill=G)
        d.text((cx + 330, T + 328), "one talk on the middle path", font=fx, fill=G)
        d.text((cx + 330, T + 356), "now an instructor · still building", font=fx, fill=G)
    if people == "friend-a":
        # far bottom-right, body giving out → ease back toward the door → climb with the agency kept
        arrow((R - 120, B - 120), (cx + 95, cy + 95), SW, 7)
        pts = damped((cx + 40, cy + 40), (R - 170, T + 150), 60, 2.5, 2.0)
        d.line(pts, fill=G, width=7, joint="curve"); arrow(pts[-3], pts[-1], G, 7)
        fb = F(26, 800); fx = F(20, 600)
        xx = cx + 380
        d.text((xx, cy + 30), "FRIEND A", font=fb, fill=INK)
        d.text((xx, cy + 64), "built his own company", font=fx, fill=SW)
        d.text((xx, cy + 92), "hated every holiday", font=fx, fill=SW)
        d.text((xx, cy + 120), "knees and elbows failing", font=fx, fill=SW)
        d.text((xx, cy + 148), "medicine had nothing", font=fx, fill=SW)
        d.text((cx + 400, T + 330), "the retreat: less doing,", font=fx, fill=G)
        d.text((cx + 400, T + 358), "more releasing, then up", font=fx, fill=G)
        d.text((cx + 400, T + 386), "still active · now feels it", font=fx, fill=G)
    if corner:
        d.ellipse([R - 34, T + 10, R - 10, T + 34], outline=INK, width=4); d.ellipse([R - 26, T + 18, R - 18, T + 26], fill=INK)
        for k, lab in enumerate(["the far corner: maximum agency", "nothing feels impossible"]):
            w = d.textlength(lab, font=fl); d.text((R - 50 - w, T + 2 + 28 * k), lab, font=fl, fill=INK if k == 0 else MID)
    for k in stickers:  # two round portraits per explained room, hugging the middle line on the right of each cell
        xx = (560 if k in ("default", "drifting") else 1380) - 110 * (len(PEOPLE[k]) - 2); yy = cy + 20 if k in ("default", "driven") else cy - 120
        for j, ph in enumerate(PEOPLE[k]): im.paste(sticker("people/" + ph), (xx + j * 110, yy))
    return im

def textslide(lines, small=None, big=64):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    f = F(big, 900); lh = int(big * 1.4); y = H // 2 - (len(lines) * lh) // 2 - (60 if small else 0)
    for l in lines:
        w = d.textlength(l, font=f); d.text(((W - w) / 2, y), l, font=f, fill=INK); y += lh
    if small:
        f2 = F(30, 500); y += 30
        for l in small:
            w = d.textlength(l, font=f2); d.text(((W - w) / 2, y), l, font=f2, fill=MID); y += 46
    return im

def twocol(title, left_h, left, right_h, right):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    f = F(60, 900); w = d.textlength(title, font=f); d.text(((W - w) / 2, 110), title, font=f, fill=INK)
    fh = F(26, 800); fb = F(26, 500)
    for x, head, lines in [(190, left_h, left), (1010, right_h, right)]:
        d.text((x, 270), head, font=fh, fill=G)
        y = 330
        for l in lines:
            d.text((x, y), ("     " + l.strip()) if l.startswith(" ") else ("·  " + l), font=fb, fill=ACC); y += 46 if l.startswith(" ") else 46
            if not l.startswith(" ") and lines.index(l) + 1 < len(lines) and not lines[lines.index(l) + 1].startswith(" "): y += 10
    return im

def wrap(d, text, font, maxw):
    words, out, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) > maxw and cur: out.append(cur); cur = w
        else: cur = trial
    if cur: out.append(cur)
    return out

def portrait(path, box=(400, 500)):
    """Greyscale, warm-tinted, centre-cropped portrait so every face sits in the same family."""
    src = Image.open(path)
    if src.mode in ("RGBA", "LA", "P"):  # transparent art: sit it on the wall colour first
        src = src.convert("RGBA"); flat = Image.new("RGBA", src.size, BG + (255,)); flat.alpha_composite(src); src = flat
    im = src.convert("L")
    bw, bh = box; iw, ih = im.size; s = max(bw / iw, bh / ih)
    im = im.resize((int(iw * s) + 1, int(ih * s) + 1))
    x0 = (im.width - bw) // 2; y0 = max(0, (im.height - bh) // 3)  # bias toward the top: faces live there
    im = im.crop((x0, y0, x0 + bw, y0 + bh))
    tint = Image.new("RGB", im.size, BG)
    return Image.blend(im.convert("RGB"), tint, 0.18)

def personslide(name, room, sub, lines, point, col, quote=None, source=None, photo=None):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    textw = 1500
    if photo:
        try:
            pt = portrait("people/" + photo); im.paste(pt, (1400, 120)); textw = 1150
            d.rectangle([1400, 120, 1799, 619], outline=INK, width=4)
        except Exception as e: print("no photo", photo, e)
    # mini quadrant glyph, with the person's room filled
    (gx, gy), gs = ((1400, 660) if photo else (W - 260, 90)), 70
    cells = {"drifting": (0, 0), "high": (1, 0), "default": (0, 1), "driven": (1, 1)}
    for k, (i, j) in cells.items():
        box = [gx + i * gs, gy + j * gs, gx + (i + 1) * gs - 6, gy + (j + 1) * gs - 6]
        d.rectangle(box, outline=MID, width=3, fill=(col if k == room else None))
    d.text((190, 120), name, font=F(72, 900), fill=INK)
    d.text((190, 215), sub, font=F(28, 600), fill=col)
    y = 300
    if quote:
        fqt = F(36, 800)
        for ql in wrap(d, "“" + quote + "”", fqt, textw):
            d.text((190, y), ql, font=fqt, fill=INK); y += 50
        if source: d.text((190, y + 4), "— " + source, font=F(22, 600), fill=MID); y += 38
        y += 34
    fb = F(28, 500)
    for l in lines:
        first = True
        for wl in wrap(d, l, fb, textw - 40):
            d.text((190, y), ("·  " if first else "    ") + wl, font=fb, fill=ACC); y += 40; first = False
        y += 14
    for pl in wrap(d, point, F(30, 800), textw):
        d.text((190, y + 24), pl, font=F(30, 800), fill=col); y += 42
    return im

def square(pts=(), whole=False, title=None, notes=(), scale=100, small_old=False, words=()):
    # 0..scale on both axes, drawn as a square; each pt = (x, y, label, col) fills the rectangle from the origin
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    X0, Y0, SIDE = 300, 170, 760; X1, Y1 = X0 + SIDE, Y0 + SIDE
    px = lambda v: X0 + SIDE * v / scale; py = lambda v: Y1 - SIDE * v / scale
    fmt = lambda n: f"{n:,}"
    d.rectangle([X0, Y0, X1, Y1], outline=MID, width=2)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for x, y, lab, col in pts:
        od.rectangle([X0, py(y), px(x), Y1], fill=col + (70,)); od.rectangle([X0, py(y), px(x), Y1], outline=col + (255,), width=4)
    if small_old:
        od.rectangle([X0, py(100), px(100), Y1], fill=INK + (90,)); od.rectangle([X0, py(100), px(100), Y1], outline=INK + (255,), width=3)
    im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im)
    for x, y, lab, col in pts:
        d.ellipse([px(x) - 9, py(y) - 9, px(x) + 9, py(y) + 9], fill=col)
        d.text((px(x) + 16, py(y) - 34), lab, font=F(24, 800), fill=col)
        d.text((px(x) + 16, py(y) - 4), f"{x} × {y} = {fmt(x * y)}", font=F(22, 600), fill=col)
    if small_old: d.text((px(100) + 12, py(100) - 6), "10,000 · the old square", font=F(20, 600), fill=INK)
    d.line([(X0, Y1), (X1, Y1)], fill=INK, width=6); d.line([(X0, Y1), (X0, Y0)], fill=INK, width=6)
    fa = F(24, 800); ft = F(22, 600)
    d.text((X0, Y1 + 14), "0", font=ft, fill=MID); d.text((X1, Y1 + 14), fmt(scale), font=ft, fill=MID, anchor="ra")
    d.text((X0 - 14, Y0), fmt(scale), font=ft, fill=MID, anchor="ra"); d.text((X0 - 14, Y1 - 24), "0", font=ft, fill=MID, anchor="ra")
    d.text(((X0 + X1) // 2, Y1 + 48), "ACTION  →", font=fa, fill=INK, anchor="ma")
    tt = Image.new("RGBA", (300, 40), (0, 0, 0, 0)); ImageDraw.Draw(tt).text((0, 0), "LETTING GO  →", font=fa, fill=INK); tt = tt.rotate(90, expand=True); im.paste(tt, (X0 - 120, (Y0 + Y1) // 2 - 150), tt)
    if whole:
        d.ellipse([X1 - 12, Y0 - 12, X1 + 12, Y0 + 12], outline=INK, width=4); d.ellipse([X1 - 4, Y0 - 4, X1 + 4, Y0 + 4], fill=INK)
        d.text((X1 - 20, Y0 + 22), f"{fmt(scale)} × {fmt(scale)} = {fmt(scale * scale)}", font=F(30, 900), fill=INK, anchor="ra")
    for i, (lw, rw) in enumerate(words):
        yy = Y0 + 95 + i * 72; fw = F(38 if i % 2 == 0 else 32, 700)
        d.text((X0 + 60, yy), lw, font=fw, fill=INK if i % 2 == 0 else MID)
        if rw: d.text((X1 - 50, yy), rw, font=fw, fill=INK if i % 2 == 0 else MID, anchor="ra")
    if title: d.text((1150, 190), title, font=F(52, 900), fill=INK)
    y = 290
    for n in notes:
        for l in wrap(d, n, F(30, 600), 700): d.text((1150, y), l, font=F(30, 600), fill=MID); y += 44
        y += 18
    return im

WORDS = [("full human potential", "samadhi"), ("the Kingdom within", "nirvana"), ("ocean of consciousness", "satori"),
         ("Jacob's ladder", "moksha"), ("stairway to heaven", "the Tao"), ("unio mystica", "fana"), ("self-transcendence", "theosis"), ("the far shore", "")]

PEOPLE = {"default": ["squidward.png", "pattyselma_sq.png", "costanza.jpg"], "driven": ["carrey.jpg", "biles.jpg"], "drifting": ["dude.jpg", "phoebe.jpg", "welwood.jpg"], "whole": ["malala.jpg", "aurelius.jpg"]}
def sticker(path, s=100):
    """Round version of portrait(), with a thin ink rim."""
    pt = portrait(path, (s, s)); m = Image.new("L", (s * 4, s * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, s * 4 - 1, s * 4 - 1], fill=255); m = m.resize((s, s), Image.LANCZOS)
    out = Image.new("RGB", (s, s), BG); out.paste(pt, (0, 0), m); ImageDraw.Draw(out).ellipse([1, 1, s - 2, s - 2], outline=INK, width=3); return out

def invite():
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    f = F(60, 900); tt = "Come once. Judge by what you feel."; d.text(((W - d.textlength(tt, font=f)) / 2, 110), tt, font=f, fill=INK)
    x, y = 160, 300
    d.text((x, y), "THE WORKSHOP", font=F(26, 800), fill=INK); y += 46
    for l in ["Saturday · 10:30 – 14:30 · $25", "Four hours, both legs: stillness, then the first step you've been avoiding.", "No beliefs required."]:
        for wl in wrap(d, l, F(30, 500), 1040): d.text((x, y), wl, font=F(30, 500), fill=MID); y += 44
    qr = Image.open("qr_meditation_club.png").convert("RGB").resize((420, 420)); im.paste(qr, (1320, 300))
    d.text((1530, 745), "Meditation Club · WhatsApp", font=F(24, 800), fill=INK, anchor="ma")
    d.text((1530, 782), "scan to join · details, questions, sign-up", font=F(22, 600), fill=MID, anchor="ma")
    return im

slides = []
slides.append(("00-title", textslide(["Why letting go", "is a high-agency skill."], ["Boring Spirituality"], big=84)))
slides.append(("01-y-axis-letting-go", render(yaxis=True)))
slides.append(("02-x-axis-agency", render(xaxis=True)))
slides.append(("03-both-axes", render(yaxis=True, xaxis=True, grid=True)))
slides.append(("03b-two-kinds-of-agency", textslide(["Two kinds of agency."], ["OUTER · doing interesting things in the world: build it, ship it, say yes, say no.", "INNER · forgive. Say sorry. Admit you were wrong. Ask for forgiveness.", "Take the first step in any emotional situation, with another person or with yourself.", "Both are actions. Only one of them is on the x-axis. The other is how you climb the y-axis on purpose."], big=64)))
slides.append(("03a-where-are-you", textslide(["Where are you?"], ["How many things did I say I would do, and then didn't?", "How often am I the first to take the first step in a conflict?", "Two questions. No belief required."], big=72)))
for i, k in enumerate(ORDER):
    slides.append((f"0{4+i}-room-{k}", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER[:i + 1], stickers=ORDER[:i])))
slides.append(("04c-patty-and-selma", personslide("Patty and Selma", "default", "The Simpsons · the female Squidwards", ["Bitter, chain-smoking, at the DMV forever.", "Every problem in their life is somebody else. Usually Homer."], "Thirty seconds. Complaining is this room's native language.", INK, photo="pattyselma.png")))
slides.append(("04d-george-costanza", personslide("George Costanza", "default", "Seinfeld · tense, passive, every fear a fact", ["Lives with his parents. Lies to avoid discomfort. Everything happens to George.", "Quits in a huff, then walks back in on Monday as if nothing happened.", "One day he does the opposite of every instinct. Gets the girl and the Yankees.", "It lasted one episode."], "The Default room has an exit: one act against the instinct. Not a new belief.", INK, quote="If every instinct you have is wrong… the opposite would have to be right.", source="Seinfeld, “The Opposite”, 1994", photo="costanza.jpg")))
slides.append(("04b-squidward", personslide("Squidward Tentacles", "default", "SpongeBob SquarePants · the joke entry, but look at him", ["Tense, bitter, passive. Hates his job, hates his neighbours, keeps both.", "Dreams of the clarinet and the gallery. Practises neither enough to leave the register.", "Every problem in his life lives next door. None of it is his to fix.", "Once moved to a town of people exactly like him. Came back.", "SpongeBob is how we all start: released, active, happy for no reason. Squidward is what fears and doubts do to it."], "Either die a SpongeBob or live long enough to become a Squidward.", INK, quote="Too bad SpongeBob isn't here to enjoy SpongeBob not being here.", source="The SpongeBob SquarePants Movie, 2004", photo="squidward.png")))
slides.append(("05b-jim-carrey", personslide("Jim Carrey", "driven", "comedian · got everything he dreamed of", ["Rich. Famous. Every dream on the list, ticked.", "His wish for everyone: the same, so they can see it isn't the answer.", "Peak reached. Room empty."], "Success amplifies the state you bring to it. It doesn't change it.", SW, quote="Everybody should get rich and famous… so they can see that it's not the answer.", source="Jim Carrey", photo="carrey.jpg")))
# swapped for Biles 2026-09-25: slides.append(("05c-michael-phelps", personslide("Michael Phelps", "driven", "28 Olympic medals · the most ever", ["After every Games, a crash. The goal gone, the reason gone with it.", "2014: days alone in a bedroom, not eating, not wanting to be alive.", "Six weeks of treatment. He had been a swimmer, not a person.", "2016: came back. Five golds. Then retired for good.", "Still has depression. Still has bad spells. Now he says so, out loud, and gets help."], "Not cured. Smaller swings, caught earlier.", SW, quote="I didn't want to be alive anymore.", source="Michael Phelps, on the weeks after London 2012", photo="phelps.jpg")))
slides.append(("05c-simone-biles", personslide("Simone Biles", "driven", "gymnast · the most decorated in history", ["Tokyo 2021: mid-air, her body stopped obeying. She pulled out of the finals.", "She said why the same day, out loud: mental health.", "Therapy. Then Paris 2024: three golds.", "Still in therapy. Still says so."], "Not cured. A smaller swing, caught earlier. The drive stayed.", SW, quote="I have to focus on my mental health.", source="Simone Biles, Tokyo, 27 July 2021", photo="biles.jpg")))
slides.append(("06b-the-dude", personslide("The Dude", "drifting", "The Big Lebowski · 1998", ["The most released man on screen. Nothing rattles him for long. He abides.", "And everything in his life happens to him: the rug, the kidnapping, the money, the car.", "Loved so much the world started a religion around him."], "Released, beloved, and carried through his own story by other people's plans.", MID, quote="The Dude abides.", source="The Big Lebowski", photo="dude.jpg")))
slides.append(("06c-phoebe-buffay", personslide("Phoebe Buffay", "drifting", "Friends · the Dude with a guitar", ["Auras, past lives, Smelly Cat. Calm, kind, loved by everyone.", "Things mostly happen to her. She is fine with that."], "The happiest resident of this room. Still a resident.", INK, photo="phoebe.jpg")))
slides.append(("06d-john-welwood", personslide("John Welwood", "drifting", "clinical psychologist and Buddhist · 1943–2019", ["Coined spiritual bypassing, 1984: using practice to sidestep the wounds you haven't faced.", "Numbness dressed as equanimity. Detachment dressed as non-attachment.", "“It's all perfect,” so you never have to feel it. Kind to everyone, honest with no one.", "His prescription: the practice AND the psychological work. Both legs."], "A Buddhist named the trap from inside. It's a diagnosis, not a dig.", MID, quote="Using spiritual ideas and practices to sidestep… unresolved emotional issues.", source="John Welwood, his definition of spiritual bypassing", photo="welwood.jpg")))
slides.append(("07e-famous-faces", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER, faces=True)))
# swapped for Malala 2026-09-25: slides.append(("07c-gandhi", personslide("Gandhi", "high", "led a nation to independence", ["The largest political movement of his century, without an army.", "One day of silence every week, for decades, while doing it.", "Spun his own cloth. Answered his own letters."], "Maximum outer agency and a daily inner practice, in the same man.", G, quote="The weak can never forgive. Forgiveness is the attribute of the strong.", source="Gandhi, Young India, 1931", photo="gandhi.jpg")))
slides.append(("07c-malala-yousafzai", personslide("Malala Yousafzai", "high", "shot at 15 for going to school · Nobel Peace Prize at 17", ["Kept going to school under the Taliban, and said so: a blog, then TV.", "Shot in the head on the school bus, 2012. Survived.", "Built a global movement for girls' education. Oxford degree.", "And the inner leg, said at the UN: she does not hate the man who shot her."], "Outer agency and inner agency in one person. Both axes, at once.", G, quote="I do not even hate the Talib who shot me.", source="Malala Yousafzai, UN Youth Assembly, 12 July 2013", photo="malala.jpg")))
slides.append(("07d-marcus-aurelius", personslide("Marcus Aurelius", "high", "Emperor of Rome · 161–180", ["Plague, a long war, a general who declared himself emperor, most of his children dead.", "At night, in a tent on campaign, notes to himself he never meant anyone to read.", "When the usurper was killed, he grieved losing the chance to pardon him."], "The biggest to-do list on earth, and present in every task on it.", G, quote="What stands in the way becomes the way.", source="Marcus Aurelius, Meditations 5.20", photo="aurelius.jpg")))
slides.append(("08f-far-corner", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER, corner=True, door=True)))
slides.append(("08-the-door", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER, corner=False, door="label", stickers=ORDER)))
slides.append(("08b-reaching-the-door", textslide(["How people reach the door."], ["From Drifting: the money runs out · life happens to them · the plateau, “nothing is changing”", "From Driven: the crash after the dream · a loss that stops the machine · a shift in values", "From an extreme you can't turn straight toward the corner. Too much inertia.", "You ease back to the middle first. Then you climb."], big=60)))
slides.append(("08d-through-the-door", textslide(["Through the door,", "life reads differently."], ["Release and action stop being two things. You feel one move the other.", "Cause and effect stop being cryptic: the conversation last Tuesday, their behaviour today.", "You notice your own state earlier. And other people's, before they say a word."], big=60)))
slides.append(("08e-life-in-the-square", twocol("Life in the high-agency square.",
    "FROM INSIDE", ["Present in what you do. Doing and noticing at once.", "Emotions arrive, are felt, and pass.", "   Reactions last minutes, not days.", "A background ease nobody can take away.", "   The inner critic is a voice in the next room.", "No unsolvable problems. If physics allows it,", "   there's a way. Decisions become experiments.", "You can receive: help, praise, rest.", "   Nothing to defend, so nothing to prove.", "Small things are vivid. Hard things are interesting."],
    "FROM OUTSIDE", ["Calm but warm. Present, not intense.", "   People say you're steadying to be around.", "The one they'd call from the jail cell.", "Direct, with kindness underneath.", "   You disagree without heat.", "You can hold someone else's storm", "   without joining it.", "They can't say what's different.", "   They want more of it."])))
slides.append(("08g-the-line", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER, corner=True, door=True, line=True)))
slides.append(("08h-visitors", textslide(["Everyone visits.", "Almost nobody lives here."], ["Athletes: in the zone. Musicians: the muse. Scientists: eureka. Founders: flow. Everyone else: gut.", "Achievers get there through work, then go back to grinding.", "Drifters get there through a retreat, a course, a plant in the jungle, then go back to the couch.", "The goal isn't to visit more often. It's to move in."], big=60)))
slides.append(("09-full-swing", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER, corner=True, door=True, swing=True)))
slides.append(("09b-friend-a-the-swing", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER, corner=True, door=True, people="friend-a")))
slides.append(("09c-friend-b-the-mirror", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER, corner=True, door=True, people="friend-b")))
slides.append(("10-the-method", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER, corner=True, door=True, swing=True, method=True)))
# cut live 2026-09-25: slides.append(("11-rule", textslide(["Development is up AND right."], ["Anyone selling you one axis is selling half.", "Productivity sells right. Most of spirituality sells up."])))
slides.append(("11-multiply", textslide(["Effectiveness ≈ release × action.", "Not plus."], ["100 active × 1 released  =  100", "95 active × 2 released  =  190", "Give up a little activity for a little release and you nearly double.", "Not a real formula. The shape is right."], big=60)))
slides.append(("11b-the-whole-square", square(whole=True, title="The whole square.", notes=["100 released. 100 active.", "100 × 100 = 10,000.", "Everything a person can be, on this chart."])))
slides.append(("11c-default-takes-100", square(pts=[(10, 10, "DEFAULT", SW)], whole=True, title="Default.", notes=["10 released × 10 active = 100.", "One percent of the square.", "Most people live here. From inside, it feels like all there is."])))
slides.append(("11d-too-far-right", square(pts=[(100, 10, "DRIVEN", SW)], whole=True, title="Too far right.", notes=["100 active × 10 released = 1,000.", "All the way to the wall. Still one tenth of the square.", "Ten times default, and it cost everything you had. The swing starts here."])))
slides.append(("11e-the-mirror", square(pts=[(100, 10, "DRIVEN", SW), (10, 100, "DRIFTING", SW)], whole=True, title="The mirror.", notes=["10 released × 100 active = 1,000.", "Same size. Different shape.", "The swing moves the same tenth around the room for years."])))
slides.append(("11f-the-aim", square(pts=[(50, 50, "the door", INK), (80, 80, "HIGH AGENCY", G)], whole=True, title="The aim.", notes=["Through the door: 50 × 50 = 2,500. A quarter of the square. Twenty-five times default.", "Further in: 80 × 80 = 6,400.", "The corner: 10,000. That is what we train for."])))
slides.append(("08c-the-gate-is-why", textslide(["The gate into the top-right", "is a question of why."], ["Drifters climb for the experience. The next state, the next insight. They plateau.", "Achievers climb for the gain. Money, status, being right. They plateau too.", "What gets through: wanting to be of use. A goal bigger than yourself.", "Change why you do what you do, and for the first time there is a reason to move at all."], big=60)))
# cut live 2026-09-25: slides.append(("12-two-legs-trained", render(yaxis=True, xaxis=True, grid=True, rooms=ORDER, corner=True, door=True, legs=True)))
# cut live 2026-09-25: slides.append(("13-reference-point", textslide(["You can't aim at a state", "you've never felt."], ["The workshop: four hours, one step into the top-right. You feel it move you. You come back a little different.", "The retreat: days inside that room, deeper than most people ever go.", "Not permanent. Shifted. And now you know what you're aiming at."])))
slides.append(("12-what-changes", textslide(["What you'll notice after."], ["How many options you see in the next hard situation.", "How long a reaction lasts: days → hours → minutes.", "The conversation you finally have.", "People asking what happened to your face."], big=60)))
slides.append(("13-zoom-out", square(scale=1000, whole=True, small_old=True, title="Now zoom out.", notes=["The far corner was the edge of the map.", "The map is bigger.", "1,000 × 1,000 = 1,000,000.", "That corner is where Anna and I are walking."])))
slides.append(("13b-the-names", square(scale=1000, whole=True, small_old=True, words=WORDS, title="Every tradition names it.", notes=["Different words. Same corner.", "Nobody owns it."])))
slides.append(("14-the-workshop", invite()))
slides.append(("15-close", textslide(["In a hard situation,", "how many options do I see?", "", "When did I last do something", "nobody asked me to do?", "", "When did I last say sorry first?"], ["release  ·  outer agency  ·  inner agency   —   answer today, answer again two weeks after"], big=56)))
os.makedirs("slides", exist_ok=True)
for f in os.listdir("slides"):
    if f.endswith(".png"): os.remove(os.path.join("slides", f))
slides.sort(key=lambda s: s[0])  # file names are the deck order
for name, im in slides: im.save(f"slides/{name}.png")
slides[0][1].save("slides/rational-spirituality-slides.pdf", save_all=True, append_images=[im for _, im in slides[1:]], resolution=144)
print("\n".join(n for n, _ in slides))
