"""Prepare the square portraits used by the essay HTML.

Run from this folder:  python prep_images.py
Reads the talk deck portraits (../talk-2026-09-25/deck/people) and the files in img/raw,
writes 360 px squares to img/ and a contact sheet to img/_contact.png.
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, '..', 'talk-2026-09-25', 'deck', 'people')
RAW = os.path.join(HERE, 'img', 'raw')
OUT = os.path.join(HERE, 'img')
SIZE = 360

# name: (source path, vertical offset 0..1 of the free space, horizontal centre 0..1, zoom 1.0 = full width)
SOURCES = {
    'squidward': (os.path.join(DECK, 'squidward.png'), 0.0, 0.5, 1.9),
    'costanza': (os.path.join(DECK, 'costanza.jpg'), 0.0, 0.5, 1.0),
    'carrey': (os.path.join(DECK, 'carrey.jpg'), 0.12, 0.5, 1.0),
    'phelps': (os.path.join(DECK, 'phelps.jpg'), 0.10, 0.5, 1.0),
    'biles': (os.path.join(DECK, 'biles.jpg'), 0.04, 0.5, 1.0),
    'dude': (os.path.join(DECK, 'dude.jpg'), 0.0, 0.5, 1.0),
    'phoebe': (os.path.join(DECK, 'phoebe.jpg'), 0.0, 0.5, 1.0),
    'welwood': (os.path.join(DECK, 'welwood.jpg'), 0.0, 0.5, 1.0),
    'malala': (os.path.join(DECK, 'malala.jpg'), 0.12, 0.5, 1.0),
    'aurelius': (os.path.join(DECK, 'aurelius.jpg'), 0.10, 0.5, 1.0),
    'hank': (os.path.join(RAW, 'hank.png'), 0.0, 0.5, 1.0),
    'jim': (os.path.join(RAW, 'jim.png'), 0.0, 0.5, 1.3),
    'pam': (os.path.join(RAW, 'pam.jpg'), 0.0, 0.5, 1.5),
    'parks': (os.path.join(RAW, 'parks.jpg'), 0.03, 0.5, 1.0),
    'thoreau': (os.path.join(RAW, 'thoreau.jpg'), 0.05, 0.5, 1.0),
    'frankl': (os.path.join(RAW, 'frankl.jpg'), 0.0, 0.5, 1.0),
    'bezos': (os.path.join(RAW, 'bezos.jpg'), 0.05, 0.5, 1.0),
    'benshahar': (os.path.join(RAW, 'benshahar.png'), 0.0, 0.5, 1.4),
}


def square(im, off, cx, zoom):
    w, h = im.size
    side = int(min(w, h) / zoom)
    side = min(side, w, h)
    x0 = int(max(0, min(w - side, cx * w - side / 2)))
    y0 = int(max(0, min(h - side, off * (h - side))))
    return im.crop((x0, y0, x0 + side, y0 + side)).resize((SIZE, SIZE), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    tiles = []
    for name, (src, off, cx, zoom) in SOURCES.items():
        im = Image.open(src)
        has_alpha = im.mode in ('RGBA', 'LA', 'P') and 'A' in im.convert('RGBA').getbands()
        im = im.convert('RGBA') if has_alpha else im.convert('RGB')
        sq = square(im, off, cx, zoom)
        if has_alpha and sq.getextrema()[3][0] < 250:
            sq.save(os.path.join(OUT, name + '.png'), optimize=True)
            ext = 'png'
        else:
            sq.convert('RGB').save(os.path.join(OUT, name + '.jpg'), quality=86, optimize=True)
            ext = 'jpg'
        tiles.append((name, os.path.join(OUT, name + '.' + ext)))
    # scooby: keep the wide frame
    sc = Image.open(os.path.join(RAW, 'scooby.png')).convert('RGB')
    sc.thumbnail((800, 450))
    sc.save(os.path.join(OUT, 'scooby.jpg'), quality=88, optimize=True)
    # contact sheet
    cols = 5
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 200, rows * 220), (235, 238, 244))
    d = ImageDraw.Draw(sheet)
    for i, (name, path) in enumerate(tiles):
        im = Image.open(path).convert('RGBA').resize((180, 180))
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        x, y = (i % cols) * 200 + 10, (i // cols) * 220 + 10
        sheet.paste(bg.convert('RGB'), (x, y))
        d.text((x, y + 184), name, fill=(20, 33, 61))
    sheet.save(os.path.join(OUT, '_contact.png'))
    print('ok', len(tiles))


if __name__ == '__main__':
    main()
