#!/usr/bin/env python3
"""Compose 'THE WORLD TODAY' — one-page newspaper front page, 1024x1024 PNG.
All text is rendered programmatically with PIL for crisp legibility."""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NOTO = "/usr/share/fonts/truetype/noto"
SERIF_BLACK = f"{NOTO}/NotoSerif-Black.ttf"
SERIF_REG = f"{NOTO}/NotoSerif-Regular.ttf"
SERIF_IT = f"{NOTO}/NotoSerif-Italic.ttf"
SANS_BOLD = f"{NOTO}/NotoSans-Bold.ttf"
SANS_SEMI = f"{NOTO}/NotoSans-SemiBold.ttf"

W = H = 1024
PAPER = (248, 244, 234)
INK = (18, 18, 18)
GREY = (90, 88, 80)
RED = (178, 30, 30)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(f, s):
    return d.textlength(s, font=f)


def fit_font(path, s, max_w, start, minimum=10):
    size = start
    while size > minimum:
        f = font(path, size)
        if text_w(f, s) <= max_w:
            return f
        size -= 1
    return font(path, minimum)


def wrap(f, s, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(f, t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def center_text(y, s, f, fill=INK):
    d.text(((W - text_w(f, s)) / 2, y), s, font=f, fill=fill)


def paste_cover(path, box, fy=0.5, inset=0.0):
    """Crop image to cover box (x0,y0,x1,y1); fy = vertical focus 0..1."""
    im = Image.open(path).convert("RGB")
    if inset:
        iw, ih = im.size
        im = im.crop((int(iw * inset), int(ih * inset),
                      int(iw * (1 - inset)), int(ih * (1 - inset))))
    bw, bh = box[2] - box[0], box[3] - box[1]
    scale = max(bw / im.width, bh / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)),
                   Image.LANCZOS)
    x = (im.width - bw) // 2
    y = int((im.height - bh) * fy)
    im = im.crop((x, y, x + bw, y + bh))
    img.paste(im, (box[0], box[1]))
    d.rectangle(box, outline=INK, width=2)


def block_text(x, y, lines, f, lh, fill=INK):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


M = 26                      # outer margin
CW = W - 2 * M              # content width = 972
COLW = (CW - 18) // 2       # 477
RX = M + COLW + 18          # right column x

# ---------------- Masthead (18..160) ----------------
d.line([(M, 16), (W - M, 16)], fill=INK, width=2)
f_mast = fit_font(SERIF_BLACK, "THE WORLD TODAY", CW, 94)
center_text(24, "THE WORLD TODAY", f_mast)
d.line([(M, 122), (W - M, 122)], fill=INK, width=6)
center_text(132, "Wednesday, 18 November 2026", font(SANS_SEMI, 21))
d.line([(M, 162), (W - M, 162)], fill=INK, width=2)

# ---------------- LEAD panel (170..512) ----------------
LY = 170
paste_cover(f"{HERE}/art_summit.png", (M, LY, W - M, LY + 198), fy=0.44)
hy = LY + 206
f_lead = fit_font(SERIF_BLACK, "ASIA'S SUMMIT DAY", CW, 56)
center_text(hy, "ASIA'S SUMMIT DAY", f_lead)
f_lsub = font(SERIF_REG, 24)
lead_sub = ("APEC opens in Shenzhen · Trump joins Quad talks in Manila · "
            "First US\u2013China\u2013Russia trilateral follows tomorrow")
sy = hy + 64
for ln in wrap(f_lsub, lead_sub, CW - 40):
    d.text(((W - text_w(f_lsub, ln)) / 2, sy), ln, font=f_lsub, fill=INK)
    sy += 30
LEAD_END = 512
d.line([(M, LEAD_END), (W - M, LEAD_END)], fill=INK, width=2)

# ---------------- Middle row: bridge + gulf (522..788) ----------------
MY = LEAD_END + 10
paste_cover(f"{HERE}/art_bridge.png", (M, MY, M + COLW, MY + 106), fy=0.52, inset=0.045)
paste_cover(f"{HERE}/art_gulf.png", (RX, MY, RX + COLW, MY + 106), fy=0.40, inset=0.02)

ty = MY + 114
f_bh = fit_font(SERIF_BLACK, "UKRAINE HITS CRIMEAN", COLW, 31)
block_text(M, ty, wrap(f_bh, "UKRAINE HITS CRIMEAN BRIDGE AGAIN", COLW), f_bh, 35)
f_gh = fit_font(SERIF_BLACK, "GULF FLARE-UP", COLW, 40)
d.text((RX, ty + 2), "GULF FLARE-UP", font=f_gh, fill=INK)

sy = ty + 74
f_sub = font(SERIF_REG, 19)
bridge_sub = ("Second day of strikes as Russia pounds Kyiv's bridges "
              "\u2014 UN: 372 civilians killed in October")
block_text(M, sy, wrap(f_sub, bridge_sub, COLW), f_sub, 24)
gulf_sub = "Iranian drones strike US radar in Bahrain \u00b7 Kuwait intercepts drones"
block_text(RX, sy, wrap(f_sub, gulf_sub, COLW), f_sub, 24)
MID_END = 788
d.line([(M + COLW + 9, MY), (M + COLW + 9, MID_END - 4)], fill=GREY, width=1)
d.line([(M, MID_END), (W - M, MID_END)], fill=INK, width=2)

# ---------------- Bottom row: markets + voyager (798..900) ----------------
BY = MID_END + 10
BH = 102
HALF = (CW - 18) // 2

cx0, cy0, cx1, cy1 = M, BY, M + 152, BY + BH
d.rectangle([cx0, cy0, cx1, cy1], fill=(252, 250, 244), outline=INK, width=2)
for gy in range(cy0 + 22, cy1 - 6, 22):
    d.line([(cx0 + 6, gy), (cx1 - 6, gy)], fill=(215, 210, 198), width=1)
pts = [(cx0 + 8, cy0 + 20), (cx0 + 32, cy0 + 16), (cx0 + 54, cy0 + 30),
       (cx0 + 74, cy0 + 26), (cx0 + 92, cy0 + 46), (cx0 + 108, cy0 + 42),
       (cx0 + 124, cy0 + 68), (cx1 - 8, cy1 - 10)]
d.line(pts, fill=RED, width=4, joint="curve")
ex, ey = pts[-1]
d.polygon([(ex, ey), (ex - 13, ey - 3), (ex - 4, ey - 13)], fill=RED)

tx = cx1 + 14
f_mh = fit_font(SERIF_BLACK, "MARKETS REEL", HALF - 166, 29)
d.text((tx, BY + 1), "MARKETS REEL", font=f_mh, fill=INK)
f_bsub = font(SERIF_REG, 17)
mkt_sub = ("Dow \u20131,000 as tech sells off before Nvidia earnings; "
           "money runs to gold")
block_text(tx, BY + 38, wrap(f_bsub, mkt_sub, HALF - 166), f_bsub, 21)

vx = M + HALF + 18
paste_cover(f"{HERE}/art_voyager.png", (vx, BY, vx + 152, BY + BH), fy=0.45)
tx2 = vx + 166
f_vh = fit_font(SERIF_BLACK, "ONE LIGHT-DAY AWAY", HALF - 166, 29)
d.text((tx2, BY + 1), "ONE LIGHT-DAY AWAY", font=f_vh, fill=INK)
voy_sub = ("Voyager 1 nears a full light-day from Earth \u2014 a first "
           "for any human-made object")
block_text(tx2, BY + 38, wrap(f_bsub, voy_sub, HALF - 166), f_bsub, 21)
d.line([(M + HALF + 9, BY), (M + HALF + 9, BY + BH)], fill=GREY, width=1)
BOT_END = BY + BH   # 900

# ---------------- ALSO TODAY strip (910..972) ----------------
AY = BOT_END + 10
f_also = font(SANS_BOLD, 18)
also = ("ALSO TODAY \u2014 Cyclone Akvan bears down on India's east coast \u00b7 "
        "Gaza ceasefire 'faces imminent collapse' \u00b7 UK sanctions settlement firms")
alines = wrap(f_also, also, CW - 32)
AH = len(alines) * 25 + 12
d.rectangle([M, AY, W - M, AY + AH], fill=INK)
yy = AY + 6
for ln in alines:
    d.text(((W - text_w(f_also, ln)) / 2, yy), ln, font=f_also, fill=PAPER)
    yy += 25

# ---------------- Footer ----------------
f_foot = font(SERIF_IT, 16)
fy_ = AY + AH + 9
center_text(fy_, "The whole day on one page \u00b7 18 Nov 2026", f_foot, fill=GREY)
assert fy_ + 22 <= H - 6, f"layout overflow: footer ends {fy_ + 22}"

out = f"{HERE}/entry.png"
img.save(out, optimize=True)
size = os.path.getsize(out)
print("saved", out, img.size, size, "bytes; strip lines:", len(alines))
if size > 1024 * 1024:
    q = img.quantize(colors=256, method=Image.MEDIANCUT,
                     dither=Image.FLOYDSTEINBERG)
    q.save(out, optimize=True)
    print("quantized ->", os.path.getsize(out), "bytes")
