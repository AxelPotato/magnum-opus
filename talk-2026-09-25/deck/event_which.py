# Square event card: the four-room chart + "Which one are you?". Run: python event_which.py -> event_which.png
from PIL import Image, ImageDraw, ImageFont
import math
FONT = "C:/Users/lelen/claude/Alex-social/Montserrat-Variable.ttf"
def F(size, w):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([w]); return f
S = 1024; BG = (234, 226, 212); INK = (47, 47, 47); MID = (120, 115, 105); ACC = (60, 60, 60)
L, T, R, B = 180, 235, 950, 860; cx, cy = (L + R) // 2, (T + B) // 2
im = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(im)

# headline
d.text((S // 2, 120), "Which one are you?", font=F(84, 900), fill=INK, anchor="mm")

# axes
d.line([(L, B), (R, B)], fill=INK, width=6); d.polygon([(R, B), (R - 20, B - 11), (R - 20, B + 11)], fill=INK)
d.line([(L, B), (L, T)], fill=INK, width=6); d.polygon([(L, T), (L - 11, T + 20), (L + 11, T + 20)], fill=INK)
fa = F(24, 800); fs = F(17, 600)
d.text((R - 8, B + 22), "ACTION  →", font=fa, fill=INK, anchor="ra")
d.text((L + 6, B + 26), "things happen to you", font=fs, fill=MID)
d.text((R - 8, B + 56), "you make things happen", font=fs, fill=MID, anchor="ra")
t = Image.new("RGBA", (420, 40), (0, 0, 0, 0)); ImageDraw.Draw(t).text((0, 0), "LETTING GO  →", font=fa, fill=INK); t = t.rotate(90, expand=True); im.paste(t, (L - 80, T + 20), t)
for lab, yy, anc in [("braced", B - 6, "ld"), ("released", T + 260, "ld")]:
    t = Image.new("RGBA", (200, 30), (0, 0, 0, 0)); ImageDraw.Draw(t).text((0, 0), lab, font=fs, fill=MID); t = t.rotate(90, expand=True); im.paste(t, (L - 46, yy - t.size[1]), t)

# dotted grid
for i in range(0, B - T, 22): d.line([(cx, T + i), (cx, min(T + i + 11, B))], fill=MID, width=3)
for i in range(0, R - L, 22): d.line([(L + i, cy), (min(L + i + 11, R), cy)], fill=MID, width=3)

# the door
rr = 54
for a in range(0, 360, 12):
    a0, a1 = math.radians(a), math.radians(a + 7)
    d.line([(cx + rr * math.cos(a0), cy + rr * math.sin(a0)), (cx + rr * math.cos(a1), cy + rr * math.sin(a1))], fill=INK, width=4)

# rooms, centred in their cells
fn = F(44, 900); fsub = F(21, 500)
cells = {"DRIFTING": ((L + cx) // 2, (T + cy) // 2, "released · passive"),
         "HIGH AGENCY": ((cx + R) // 2, (T + cy) // 2, "released · active"),
         "DEFAULT": ((L + cx) // 2, (cy + B) // 2, "tense · passive"),
         "DRIVEN": ((cx + R) // 2, (cy + B) // 2, "tense · active")}
for name, (x, y, sub) in cells.items():
    d.text((x, y - 18), name, font=fn, fill=INK, anchor="mm"); d.text((x, y + 30), sub, font=fsub, fill=ACC, anchor="mm")

# tag
d.text((S // 2, 972), "B O R I N G   S P I R I T U A L I T Y", font=F(22, 800), fill=MID, anchor="mm")
im.save("event_which.png"); print("ok")
