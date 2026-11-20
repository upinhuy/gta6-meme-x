#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: 'Making room for GTA VI (200 GB)'.
The make.fun ghost mascot is drawn from scratch per the official description:
white ghost, thick black outline, two black four-pointed sparkle eyes, a round
little hand, holding a magenta coin with a white star.
Rendered at 2x and downscaled for clean edges. Output: meme.png (1200x1200).
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

S = 2                      # supersample factor
W = 1200 * S
H = 1200 * S
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size * S)

def fit_font(draw, text, path, start_size, max_w, stroke=0):
    size = start_size
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) + 2 * stroke * S <= max_w * S:
            return f
        size -= 2
    return font(path, size)

def ctext(draw, cx, y, text, f, fill, stroke=0, stroke_fill=(0, 0, 0)):
    draw.text((cx * S, y * S), text, font=f, fill=fill, anchor="ma",
              stroke_width=stroke * S, stroke_fill=stroke_fill)

# ---------- background: Vice City night gradient + skyline ----------
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

top_c, mid_c, bot_c = (22, 10, 46), (43, 16, 82), (16, 8, 31)
bg = Image.new("RGB", (W, H))
bd = ImageDraw.Draw(bg)
for yy in range(H):
    t = yy / H
    col = lerp(top_c, mid_c, t / 0.55) if t < 0.55 else lerp(mid_c, bot_c, (t - 0.55) / 0.45)
    bd.line([(0, yy), (W, yy)], fill=col)
img = bg.convert("RGBA")
d = ImageDraw.Draw(img, "RGBA")

# stars
import random
random.seed(6)
for _ in range(90):
    x, y = random.uniform(0, W), random.uniform(0, H * 0.42)
    r = random.uniform(1, 2.6) * S
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 120))

# neon horizon glow
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-300 * S, 700 * S, 1500 * S, 1250 * S], fill=(255, 46, 136, 60))
img = Image.alpha_composite(img, glow)
d = ImageDraw.Draw(img, "RGBA")

# skyline silhouette along the bottom
random.seed(11)
x = -20
while x < 1240:
    bw = random.randint(60, 130)
    bh = random.randint(60, 130)
    d.rectangle([x * S, (1200 - bh) * S, (x + bw) * S, 1200 * S], fill=(10, 5, 24, 235))
    for _ in range(int(bw * bh / 900)):
        wx, wy = x + random.uniform(6, bw - 10), 1200 - bh + random.uniform(8, bh - 14)
        d.rectangle([wx * S, wy * S, (wx + 4) * S, (wy + 6) * S],
                    fill=random.choice([(39, 232, 255, 200), (255, 210, 63, 200), (255, 46, 136, 180)]))
    x += bw + random.randint(4, 18)
d = ImageDraw.Draw(img, "RGBA")

# ---------- top captions ----------
f1 = fit_font(d, "MAKING ROOM FOR GTA VI", BOLD, 92, 1120, stroke=6)
ctext(d, 600, 26, "MAKING ROOM FOR GTA VI", f1, (255, 255, 255), stroke=6)
f2 = fit_font(d, "— 200 GB INCOMING —", BOLD, 54, 800)
ctext(d, 600, 138, "— 200 GB INCOMING —", f2, (39, 232, 255), stroke=4)

# ---------- helpers ----------
def sparkle(cx, cy, R, r, fill):
    pts = []
    for i in range(8):
        ang = -math.pi / 2 + i * math.pi / 4
        rad = R if i % 2 == 0 else r
        pts.append(((cx + rad * math.cos(ang)) * S, (cy + rad * math.sin(ang)) * S))
    d.polygon(pts, fill=fill)

def star5(cx, cy, R, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else R * 0.45
        pts.append(((cx + rad * math.cos(ang)) * S, (cy + rad * math.sin(ang)) * S))
    d.polygon(pts, fill=fill)

def folder(cx, cy, w, h, label, sub=None, angle=0, body=(255, 179, 64), tab=(255, 201, 102)):
    lay = Image.new("RGBA", (int(w * 1.3 * S), int(h * 1.5 * S)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ox, oy = lay.width // 2, lay.height // 2
    X0, Y0 = ox - w * S / 2, oy - h * S / 2
    # tab
    ld.rounded_rectangle([X0, Y0, X0 + w * S * 0.42, Y0 + h * S * 0.30], radius=10 * S,
                         fill=tab, outline=(0, 0, 0), width=5 * S)
    # body
    ld.rounded_rectangle([X0, Y0 + h * S * 0.16, X0 + w * S, Y0 + h * S], radius=14 * S,
                         fill=body, outline=(0, 0, 0), width=5 * S)
    fl = fit_font(ld, label, BOLD, int(h * 0.30), w * 0.88)
    ld.text((ox, Y0 + h * S * (0.34 if sub else 0.40)), label, font=fl,
            fill=(26, 16, 48), anchor="ma")
    if sub:
        fs = fit_font(ld, sub, BOLD, int(h * 0.20), w * 0.88)
        ld.text((ox, Y0 + h * S * 0.66), sub, font=fs, fill=(26, 16, 48), anchor="ma")
    if angle:
        lay = lay.rotate(angle, resample=Image.BICUBIC, center=(ox, oy))
    img.alpha_composite(lay, (int((cx - lay.width / S / 2) * S), int((cy - lay.height / S / 2) * S)))
    globals()['d'] = ImageDraw.Draw(img, "RGBA")

# ---------- trash bin (right) with doomed folders ----------
binx0, binx1, biny0, biny1 = 815, 1130, 585, 905
d.polygon([(binx0 * S, biny0 * S), (binx1 * S, biny0 * S), ((binx1 - 28) * S, biny1 * S), ((binx0 + 28) * S, biny1 * S)],
          fill=(122, 133, 158), outline=(0, 0, 0), width=6 * S)
for i in range(1, 5):
    xx = binx0 + (binx1 - binx0) * i / 5
    d.line([(xx * S, (biny0 + 26) * S), ((xx - 8) * S, (biny1 - 18) * S)], fill=(84, 94, 116), width=7 * S)
d.rounded_rectangle([(binx0 - 14) * S, (biny0 - 22) * S, (binx1 + 14) * S, (biny0 + 10) * S],
                    radius=10 * S, fill=(150, 162, 188), outline=(0, 0, 0), width=6 * S)
folder(872, 528, 205, 112, "GTA V", "2013", angle=10)
folder(1072, 522, 235, 112, "FAMILY", "PHOTOS", angle=-8)
folder(1058, 418, 230, 108, "WORK", "FILES", angle=7)
folder(878, 420, 185, 104, "SLEEP", None, angle=-13)

# ---------- the ghost (centre-left), drawn from scratch ----------
# magenta disc glow behind the ghost
disc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dd = ImageDraw.Draw(disc)
dd.ellipse([70 * S, 250 * S, 700 * S, 880 * S], fill=(255, 46, 166, 46))
img = Image.alpha_composite(img, disc)
d = ImageDraw.Draw(img, "RGBA")

gx, gy, gw, gh = 385, 545, 350, 330   # ghost centre x, centre y, width, height
def ghost_points(scale=1.0):
    pts = []
    cx, top = gx, gy - gh / 2
    r = gw / 2
    for i in range(25):                       # dome
        ang = math.pi - (math.pi * i / 24)
        pts.append((cx + scale * r * math.cos(ang), gy - gh * 0.08 - scale * (gh * 0.42) * math.sin(ang)))
    ybot = gy + gh / 2
    pts.append((cx + scale * r, ybot - 26))
    bumps = 4
    for b in range(bumps):                    # wavy hem
        bx0 = cx + r - (2 * r) * b / bumps
        for i in range(1, 9):
            ang = math.pi * i / 8
            pts.append((bx0 - (2 * r / bumps) * i / 8, ybot - 26 + 26 * math.sin(ang) * scale))
    pts.append((cx - scale * r, ybot - 26))
    return [(x * S, y * S) for x, y in pts]

d.polygon(ghost_points(1.0), fill=(0, 0, 0))            # thick black outline layer
inset = [(gx * S + (x - gx * S) * 0.90, (gy - 8) * S + (y - (gy - 8) * S) * 0.94) for x, y in ghost_points(1.0)]
d.polygon(inset, fill=(255, 255, 255))
# sparkle eyes
sparkle(gx - 62, gy - 95, 34, 7, (0, 0, 0))
sparkle(gx + 62, gy - 95, 34, 7, (0, 0, 0))
# smile
d.arc([(gx - 34) * S, (gy - 62) * S, (gx + 34) * S, (gy - 6) * S], start=15, end=165,
      fill=(0, 0, 0), width=7 * S)
# cheek blush
d.ellipse([(gx - 128) * S, (gy - 48) * S, (gx - 84) * S, (gy - 22) * S], fill=(255, 150, 200))
d.ellipse([(gx + 84) * S, (gy - 48) * S, (gx + 128) * S, (gy - 22) * S], fill=(255, 150, 200))

# hugged folder: make.fun earnings (the keeper)
folder(400, 742, 330, 168, "make.fun", "earnings", angle=-3)
# ghost's round little hand over the folder
d.ellipse([(505) * S, (672) * S, (565) * S, (728) * S], fill=(255, 255, 255), outline=(0, 0, 0), width=6 * S)

# magenta star coin (top-left of ghost), then the round little hand holding it
d.ellipse([(83) * S, (218) * S, (247) * S, (382) * S], fill=(255, 46, 166), outline=(0, 0, 0), width=7 * S)
star5(165, 300, 52, (255, 255, 255))
d.ellipse([(205) * S, (330) * S, (269) * S, (392) * S], fill=(255, 255, 255), outline=(0, 0, 0), width=6 * S)

# ---------- storage bar ----------
bar_x0, bar_x1, bar_y = 95, 1105, 952
d.rounded_rectangle([bar_x0 * S, bar_y * S, bar_x1 * S, (bar_y + 54) * S], radius=16 * S,
                    outline=(255, 255, 255), width=5 * S)
fillw = (bar_x1 - bar_x0 - 16) * 0.99
d.rounded_rectangle([(bar_x0 + 8) * S, (bar_y + 8) * S, (bar_x0 + 8 + fillw) * S, (bar_y + 46) * S],
                    radius=11 * S, fill=(255, 46, 100))
fb = fit_font(d, "STORAGE 99% FULL", BOLD, 40, 700)
ctext(d, 600, bar_y + 9, "STORAGE 99% FULL", fb, (255, 255, 255), stroke=3)

# ---------- bottom caption ----------
d.rounded_rectangle([40 * S, 1018 * S, 1160 * S, 1192 * S], radius=18 * S, fill=(8, 4, 18, 165))
f3 = fit_font(d, "EVERYTHING GOES.", BOLD, 66, 1050, stroke=5)
ctext(d, 600, 1030, "EVERYTHING GOES.", f3, (255, 255, 255), stroke=5)
f4 = fit_font(d, "Except the folder paying for it.", BOLD, 56, 1050, stroke=5)
ctext(d, 600, 1108, "Except the folder paying for it.", f4, (255, 210, 63), stroke=5)

img = img.convert("RGB").resize((1200, 1200), Image.LANCZOS)
img.save(OUT, "PNG")
img.resize((480, 480), Image.LANCZOS).save("/tmp/meme-480.png", "PNG")
print("saved", OUT, os.path.getsize(OUT), "bytes")
