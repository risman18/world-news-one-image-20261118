#!/usr/bin/env python3
"""Compose 'THE WORLD TODAY' v2 — vintage broadsheet front page, 1024x1024 PNG.
Format per Risman's reference: huge masthead, info bar between double rules,
giant BREAKING NEWS banner, lead story with photo right / text left and a
pull-quote box, then four stories in columns below. Navy ink throughout.
All text is rendered programmatically with PIL; display text is placed by its
measured ink box so nothing overlaps."""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NOTO = "/usr/share/fonts/truetype/noto"
COND_BLACK = f"{NOTO}/NotoSansDisplay-CondensedBlack.ttf"
SERIF_BLACK = f"{NOTO}/NotoSerif-Black.ttf"
SERIF_REG = f"{NOTO}/NotoSerif-Regular.ttf"
SERIF_IT = f"{NOTO}/NotoSerif-Italic.ttf"
SANS_BOLD = f"{NOTO}/NotoSans-Bold.ttf"

W = H = 1024
PAPER = (248, 244, 234)
NAVY = (22, 41, 77)          # #16294d
INK = (24, 24, 28)
GREY = (96, 94, 86)
LGREY = (198, 194, 184)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(f, s):
    return d.textlength(s, font=f)


def ink(f, s):
    """(top_offset, ink_height) of string s in font f."""
    b = d.textbbox((0, 0), s, font=f)
    return b[1], b[3] - b[1]


def fit_font(path, s, max_w, start, minimum=10):
    size = start
    while size > minimum:
        f = font(path, size)
        if text_w(f, s) <= max_w:
            return f, size
        size -= 1
    return font(path, minimum), minimum


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


def center_ink(y, s, f, fill=NAVY):
    """Draw s horizontally centered with its ink top at y; return ink bottom."""
    off, ih = ink(f, s)
    d.text(((W - text_w(f, s)) / 2, y - off), s, font=f, fill=fill)
    return y + ih


def left_ink(x, y, s, f, fill=NAVY):
    off, ih = ink(f, s)
    d.text((x, y - off), s, font=f, fill=fill)
    return y + ih


def double_rule(y, w_top=2, w_bot=5, gap=3):
    d.line([(M, y), (W - M, y)], fill=NAVY, width=w_top)
    d.line([(M, y + w_top + gap), (W - M, y + w_top + gap)], fill=NAVY, width=w_bot)
    return y + w_top + gap + w_bot


def paste_cover(path, box, fy=0.5, inset=0.0):
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
    yy = int((im.height - bh) * fy)
    im = im.crop((x, yy, x + bw, yy + bh))
    img.paste(im, (box[0], box[1]))
    d.rectangle(box, outline=NAVY, width=2)


def block_text(x, y, lines, f, lh, fill=INK):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


M = 26
CW = W - 2 * M               # 972

# ---------------- Top double rule + masthead ----------------
y = double_rule(12)                                   # ends 22
f_mast, ms = fit_font(COND_BLACK, "THE WORLD TODAY", CW, 150)
y = center_ink(28, "THE WORLD TODAY", f_mast)         # ink bottom ~118
print("masthead size", ms, "ink bottom", y)

# ---------------- Info bar between double rules ----------------
y = double_rule(y + 4, w_top=5, w_bot=2)
f_info = font(SANS_BOLD, 19)
info = "VOL. 1 \u00b7 NO. 324    *    WEDNESDAY, 18 NOVEMBER 2026    *    ONE DAY \u00b7 ONE PAGE"
y = center_ink(y + 6, info, f_info)
y = double_rule(y + 6, w_top=2, w_bot=5)
print("after info bar", y)

# ---------------- BREAKING NEWS banner ----------------
f_ban, bs = fit_font(COND_BLACK, "BREAKING NEWS", CW, 122)
y = center_ink(y + 10, "BREAKING NEWS", f_ban)
print("banner size", bs, "ink bottom", y)
y = double_rule(y + 4, w_top=5, w_bot=2)

# ---------------- LEAD block ----------------
LEAD_Y = y + 10
LX, LW = M, 462                    # left text column
RX = M + LW + 18                   # 506
RW = W - M - RX                    # 492

f_kick = font(SANS_BOLD, 17)
ky = left_ink(LX, LEAD_Y, "LEAD STORY \u2014 SHENZHEN", f_kick)
f_lh, lhs = fit_font(SERIF_BLACK, "ASIA'S SUMMIT DAY", LW, 54)
hy = left_ink(LX, ky + 8, "ASIA'S SUMMIT DAY", f_lh)
print("lead headline size", lhs, "bottom", hy)
f_body = font(SERIF_REG, 19)
lead_body = ("Xi Jinping opened the APEC summit in Shenzhen with a pledge "
             "of tariff cuts and wider market access, and leaders issued "
             "the first-ever Shenzhen Initiative. Donald Trump arrived to "
             "a welcome from Xi and shook hands with Vladimir Putin. Today "
             "the three meet \u2014 the first US\u2013China\u2013Russia "
             "trilateral in history.")
lead_lines = wrap(f_body, lead_body, LW)
by = block_text(LX, hy + 10, lead_lines, f_body, 21)
print("lead body lines", len(lead_lines), "ends", by)

qy = by + 8
f_quote = font(SERIF_IT, 20)
quote = ("\u201cTODAY \u2014 Trump, Xi and Putin sit down together in "
         "Shenzhen, the first trilateral of the three nuclear powers. "
         "No deal is expected.\u201d")
qlines = wrap(f_quote, quote, LW - 30)
qh = len(qlines) * 23 + 14
d.rectangle([LX, qy, LX + LW, qy + qh], outline=NAVY, width=3)
block_text(LX + 15, qy + 7, qlines, f_quote, 23, fill=NAVY)
LEAD_END = qy + qh

paste_cover(f"{HERE}/art_summit.png", (RX, LEAD_Y, RX + RW, LEAD_Y + 272), fy=0.44)
f_cap = font(SERIF_IT, 17)
cap = ("Trump arrived in Shenzhen on Wednesday, welcomed by Xi at the "
       "airport \u2014 the three leaders meet today.")
cy = LEAD_Y + 280
for ln in wrap(f_cap, cap, RW):
    d.text((RX, cy), ln, font=f_cap, fill=GREY)
    cy += 21
LEAD_END = max(LEAD_END, cy)
print("lead ends", LEAD_END)
assert LEAD_END <= 648, LEAD_END

# ---------------- Rule + four story columns ----------------
RY = LEAD_END + 10
d.line([(M, RY), (W - M, RY)], fill=NAVY, width=2)
SY = RY + 10
COLW = (CW - 3 * 16) // 4          # 231
COLS_X = [M + i * (COLW + 16) for i in range(4)]
ART_H = 38

stories = [
    ("UKRAINE HITS CRIMEAN BRIDGE AGAIN", "art_bridge.png", 0.52,
     "Ukraine's assault brought the Crimean Bridge's road arch crashing "
     "into the Kerch Strait, the worst damage since it opened in 2018. "
     "Two were killed; rail partly resumed. Moscow vowed to rebuild "
     "before Putin meets Trump and Xi."),
    ("GULF FLARE-UP", "art_gulf.png", 0.40,
     "Iranian drones hit a US radar in Bahrain, and US jets struck an "
     "Iranian missile site on Qeshm Island. Kuwait's defences then "
     "countered drones of their own, and an ADNOC ship was attacked in "
     "the Strait of Hormuz."),
    ("MARKETS REEL", None, 0.0,
     "The Dow fell 561 points and the S&P slid for a fifth straight day "
     "as Fed minutes pointed to a December rate rise. Nvidia beat "
     "forecasts \u2014 $115.8bn in sales \u2014 then fell 2.9% anyway, "
     "while the Nasdaq rose."),
    ("ONE LIGHT-DAY AWAY", "art_voyager.png", 0.45,
     "Forty-nine years after launch, Voyager 1 crossed one light-day "
     "from Earth at 10:16 UTC \u2014 25.9 billion kilometres out, the "
     "first human-made object to get there. Its signals home now take "
     "a full day."),
]

f_col_h = font(SERIF_BLACK, 20)
f_col_b = font(SERIF_REG, 17)
head_wrapped = [wrap(f_col_h, s[0], COLW) for s in stories]
HZONE = max(len(h) for h in head_wrapped) * 21
BODY_Y = SY + ART_H + 8 + HZONE + 2
print("headline zone", HZONE, "body starts", BODY_Y)
for i, (head, art, fy_, body) in enumerate(stories):
    x = COLS_X[i]
    if art:
        paste_cover(f"{HERE}/{art}", (x, SY, x + COLW, SY + ART_H), fy=fy_)
    else:
        box = [x, SY, x + COLW, SY + ART_H]
        d.rectangle(box, fill=(252, 250, 244), outline=NAVY, width=2)
        for gy in range(SY + 10, SY + ART_H - 3, 9):
            d.line([(x + 5, gy), (x + COLW - 5, gy)], fill=LGREY, width=1)
        pts = [(x + 7, SY + 7), (x + 42, SY + 6), (x + 74, SY + 12),
               (x + 104, SY + 9), (x + 132, SY + 19), (x + 158, SY + 16),
               (x + 186, SY + 27), (x + COLW - 7, SY + ART_H - 5)]
        d.line(pts, fill=NAVY, width=3, joint="curve")
        ex, ey = pts[-1]
        d.polygon([(ex, ey), (ex - 11, ey - 2), (ex - 3, ey - 11)], fill=NAVY)
    block_text(x, SY + ART_H + 8, head_wrapped[i], f_col_h, 21, fill=NAVY)
    blines = wrap(f_col_b, body, COLW)
    bend = block_text(x, BODY_Y, blines, f_col_b, 20)
    print("col", i, head[:18], "body lines", len(blines), "ends", bend)
    assert bend <= 950, (i, bend)
    if i < 3:
        dx = x + COLW + 8
        d.line([(dx, SY), (dx, 948)], fill=LGREY, width=1)

# ---------------- Footer: navy ALSO TODAY strip ----------------
FY = 956
f_also = font(SANS_BOLD, 17)
also = ("ALSO TODAY \u2014 Cyclone Akvan crawls toward India's east coast, "
        "landfall due Friday \u00b7 Gaza ceasefire 'faces imminent collapse' "
        "\u00b7 UK sanctions settlement firms")
alines = wrap(f_also, also, CW - 36)
AH = len(alines) * 21 + 12
assert FY + AH <= H - 8, (FY, AH)
d.rectangle([M, FY, W - M, FY + AH], fill=NAVY)
yy = FY + 6
for ln in alines:
    d.text(((W - text_w(f_also, ln)) / 2, yy), ln, font=f_also, fill=PAPER)
    yy += 21

out = f"{HERE}/entry.png"
img.save(out, optimize=True)
size = os.path.getsize(out)
print("saved", out, img.size, size, "bytes; also lines:", len(alines))
if size > 1024 * 1024:
    q = img.quantize(colors=256, method=Image.MEDIANCUT,
                     dither=Image.FLOYDSTEINBERG)
    q.save(out, optimize=True)
    print("quantized ->", os.path.getsize(out), "bytes")
