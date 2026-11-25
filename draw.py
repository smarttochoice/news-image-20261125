#!/usr/bin/env python3
"""Draw the entry image: a one-page newspaper front page summing up the
world news of Wednesday 25 November 2026.

Everything is drawn with PIL primitives and set in DejaVu; no photos, no
network, no fetched assets. Re-running this file reproduces entry.png
byte-for-byte. Output: entry.png, 1024x1024, under 1 MiB."""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 239)
INK = (22, 22, 22)
NAVY = (18, 44, 88)
CRIMSON = (176, 32, 32)
GOLD = (182, 136, 42)
GREEN = (12, 100, 36)
TEAL = (13, 94, 90)
GREY = (98, 98, 98)
CARD = (255, 255, 255)
CREAM = (239, 232, 217)
SKY = (64, 128, 180)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def serif_b(size):
    return ImageFont.truetype(FDIR + "DejaVuSerif-Bold.ttf", size)


def serif(size):
    return ImageFont.truetype(FDIR + "DejaVuSerif.ttf", size)


def sans_b(size):
    return ImageFont.truetype(FDIR + "DejaVuSans-Bold.ttf", size)


def sans(size):
    return ImageFont.truetype(FDIR + "DejaVuSans.ttf", size)


def wrap_lines(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    out, cur = [], ""
    for word in text.split():
        cand = word if not cur else cur + " " + word
        if d.textlength(cand, font=font) <= max_w:
            cur = cand
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, x, y, text, font, max_w, fill=INK, gap=None):
    """Draw wrapped text; return the y just past the last line."""
    step = gap if gap is not None else int(font.size * 1.3)
    for line in wrap_lines(d, text, font, max_w):
        d.text((x, y), line, font=font, fill=fill)
        y += step
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead: paper-white band, black serif nameplate, red dateline -----
d.rectangle([0, 0, W, 108], fill=CARD)
d.rectangle([0, 108, W, 112], fill=INK)
d.text((512, 6), "THE WORLD TODAY", font=serif_b(52), fill=INK, anchor="ma")
d.text((512, 66), "WEDNESDAY  ·  25 NOVEMBER 2026", font=sans_b(25),
       fill=CRIMSON, anchor="ma")

# ---- hero: Ukraine drone strike on a Russian ship -------------------------
hx, hy, hw, hh = 24, 124, W - 48, 272
d.rectangle([hx, hy, hx + hw, hy + hh], outline=INK, width=3, fill=CARD)
d.rectangle([hx, hy, hx + hw, hy + 8], fill=NAVY)
# ship + drone pictogram, left
sx, sy = 60, 210
d.polygon([(sx, sy + 46), (sx + 26, sy + 46), (sx + 20, sy + 78),
           (sx + 150, sy + 78), (sx + 172, sy + 46)], fill=NAVY,
          outline=INK)
d.rectangle([sx + 52, sy + 14, sx + 112, sy + 46], fill=CRIMSON,
            outline=INK)
d.rectangle([sx + 76, sy - 6, sx + 84, sy + 14], fill=INK)
d.arc([sx + 8, sy + 84, sx + 60, sy + 106], 0, 180, fill=SKY, width=5)
d.arc([sx + 60, sy + 84, sx + 112, sy + 106], 0, 180, fill=SKY, width=5)
d.arc([sx + 112, sy + 84, sx + 164, sy + 106], 0, 180, fill=SKY, width=5)
# drone above the ship
dx, dy = 150, 156
d.ellipse([dx - 8, dy - 8, dx + 8, dy + 8], fill=INK)
d.line([(dx - 26, dy - 14), (dx + 26, dy - 14)], fill=INK, width=3)
d.line([(dx - 26, dy + 14), (dx + 26, dy + 14)], fill=INK, width=3)
d.ellipse([dx - 34, dy - 20, dx - 18, dy - 8], outline=INK, width=2)
d.ellipse([dx + 18, dy - 20, dx + 34, dy - 8], outline=INK, width=2)
d.ellipse([dx - 34, dy + 8, dx - 18, dy + 20], outline=INK, width=2)
d.ellipse([dx + 18, dy + 8, dx + 34, dy + 20], outline=INK, width=2)
burst = []
for i in range(10):
    ang = i * math.pi / 5
    r = 24 if i % 2 == 0 else 9
    burst.append((dx + 76 + r * math.cos(ang), dy + 22 + r * math.sin(ang)))
d.polygon(burst, fill=(255, 190, 40), outline=INK)
# hero copy
tx = 300
d.text((tx, hy + 20), "WAR  •  GULF OF FINLAND", font=sans_b(20), fill=NAVY)
d.text((tx, hy + 50), "Ukraine strikes Russian", font=serif_b(40), fill=INK)
d.text((tx, hy + 98), "cargo ship off Finland", font=serif_b(40), fill=INK)
para(d, tx, hy + 158,
     "Zelenskiy confirms Kyiv carried out the drone strike; Norway urges "
     "caution and Moscow calls it \u201cterrorism\u201d.",
     serif(23), hw - (tx - hx) - 24, gap=30)
d.text((tx, hy + 240), "A second Russian warship was hit off Benghazi, Libya.",
       font=sans_b(19), fill=CRIMSON)

# ---- story cards ----------------------------------------------------------
gx, gy = 24, 410
pw, ph, gap = 304, 238, 14


def card(col, row, strip, kicker, head, summ, draw_icon, tag):
    x = gx + col * (pw + gap)
    y = gy + row * (ph + gap)
    d.rectangle([x, y, x + pw, y + ph], outline=INK, width=2, fill=CARD)
    d.rectangle([x, y, x + pw, y + 8], fill=strip)
    d.text((x + 14, y + 18), kicker, font=sans_b(15), fill=strip)
    draw_icon(x, y)
    d.text((x + 118, y + 52), tag, font=serif_b(24), fill=INK)
    end = para(d, x + 14, y + 98, head, serif_b(20), pw - 28, gap=25)
    para(d, x + 14, end + 6, summ, sans(15), pw - 28, gap=19)


def icon_fall(x, y):
    bx, by = x + 18, y + 44
    heights = [46, 36, 26, 14]
    for i, h in enumerate(heights):
        d.rectangle([bx + i * 24, by + 46 - h, bx + i * 24 + 16, by + 46],
                    fill=CRIMSON if i else NAVY)
    d.line([(bx - 2, by + 46), (bx + 96, by + 46)], fill=INK, width=2)
    d.line([(bx + 4, by + 4), (bx + 92, by + 34)], fill=CRIMSON, width=4)
    d.polygon([(bx + 92, by + 34), (bx + 78, by + 30), (bx + 88, by + 44)],
              fill=CRIMSON)


def icon_ruin(x, y):
    bx, by = x + 22, y + 44
    d.rectangle([bx, by, bx + 34, by + 48], fill=(150, 150, 150), outline=INK)
    d.rectangle([bx + 40, by + 12, bx + 74, by + 48], fill=(120, 120, 120),
                outline=INK)
    d.line([(bx + 40, by + 12), (bx + 57, by + 30), (bx + 40, by + 48)],
           fill=CRIMSON, width=3)
    d.ellipse([bx + 4, by + 10, bx + 20, by + 26], fill=(200, 200, 200),
              outline=GREY)
    d.ellipse([bx + 54, by - 2, bx + 70, by + 14], fill=(200, 200, 200),
              outline=GREY)


def icon_rocket(x, y):
    rx, ry = x + 58, y + 72
    d.ellipse([rx - 52, ry - 22, rx + 52, ry + 22], outline=SKY, width=3)
    d.polygon([(rx - 10, ry - 28), (rx + 10, ry - 28), (rx + 12, ry + 6),
               (rx - 12, ry + 6)], fill=CRIMSON, outline=INK)
    d.polygon([(rx - 10, ry - 28), (rx, ry - 38), (rx + 10, ry - 28)],
              fill=NAVY)
    d.polygon([(rx - 12, ry + 6), (rx - 4, ry + 6), (rx - 8, ry + 20)],
              fill=(255, 160, 40), outline=INK)
    d.polygon([(rx + 4, ry + 6), (rx + 12, ry + 6), (rx + 8, ry + 20)],
              fill=(255, 160, 40), outline=INK)
    d.ellipse([rx + 34, ry + 16, rx + 42, ry + 24], fill=GOLD)


def icon_tower(x, y):
    tx0, ty0 = x + 40, y + 52
    d.polygon([(tx0, ty0), (tx0 + 36, ty0), (tx0 + 30, ty0 + 40),
               (tx0 + 6, ty0 + 40)], fill=NAVY, outline=INK)
    d.polygon([(tx0 + 10, ty0 - 6), (tx0 + 18, ty0 - 14),
               (tx0 + 26, ty0 - 6)], fill=CRIMSON, outline=INK)
    for j in range(3):
        d.rectangle([tx0 + 10, ty0 + 6 + j * 11, tx0 + 26, ty0 + 12 + j * 11],
                    fill=(255, 220, 120))
    burst2 = []
    for i in range(10):
        ang = i * math.pi / 5
        r = 14 if i % 2 == 0 else 6
        burst2.append((tx0 + 58 + r * math.cos(ang),
                       ty0 + 2 + r * math.sin(ang)))
    d.polygon(burst2, fill=(255, 190, 40), outline=INK)


def icon_court(x, y):
    cx0, cy0 = x + 22, y + 48
    d.polygon([(cx0, cy0), (cx0 + 76, cy0), (cx0 + 38, cy0 - 14)],
              fill=NAVY, outline=INK)
    for i in range(3):
        d.rectangle([cx0 + 6 + i * 26, cy0 + 6, cx0 + 18 + i * 26, cy0 + 40],
                    fill=(200, 200, 200), outline=INK)
    d.rectangle([cx0, cy0 + 40, cx0 + 76, cy0 + 46], fill=INK)


card(0, 0, CRIMSON, "MARKETS  •  USA",
     "AI trade collapses after Nvidia surge",
     "Nasdaq -1.5%, Nvidia -6%, Micron -11% a day after a 31% jump; the US "
     "is said to plan tariff hikes on China, the EU and 14 economies.",
     icon_fall, "-6%")
card(1, 0, (120, 84, 20), "WAR  •  GAZA",
     "Israeli strike kills Hamas security chief",
     "Naeem Abu Nahel is killed in Gaza; at least seven Palestinians die "
     "on Tuesday.",
     icon_ruin, "7 dead")
card(2, 0, NAVY, "SPACE  •  CHINA",
     "Pakistan's first astronaut reaches orbit",
     "Muhammad Zeeshan Ali launches aboard Shenzhou-24 to Tiangong — the "
     "first Pakistani in space, and the station's first foreign astronaut.",
     icon_rocket, "1st")
card(0, 1, (90, 40, 40), "WAR  •  RIYADH",
     "Houthis hit Riyadh's tallest tower",
     "Eleven people are wounded in the strike on the capital's tallest "
     "tower; the Houthis threaten Saudi ports.",
     icon_tower, "11 hurt")
card(1, 1, TEAL, "COURTS  •  USA",
     "Huawei guilty of trade-secret theft",
     "A US jury convicts Huawei of stealing trade secrets; it is acquitted "
     "of racketeering.",
     icon_court, "Guilty")

# ---- also today -----------------------------------------------------------
ax = gx + 2 * (pw + gap)
ay = gy + 1 * (ph + gap)
d.rectangle([ax, ay, ax + pw, ay + ph], outline=INK, width=2, fill=CREAM)
d.rectangle([ax, ay, ax + pw, ay + 8], fill=GOLD)
d.text((ax + 14, ay + 18), "ALSO TODAY", font=sans_b(15), fill=(120, 84, 20))
extra = [
    "COP31 climate summit in Antalya collapses with no deal.",
    "Sarkozy and Carla Bruni ordered to stand trial in a corruption case.",
    "Nepal hit by a 5.6-magnitude earthquake.",
    "Malaysia to return 6,500+ Rohingya refugees to Myanmar in December.",
]
yy = ay + 46
for item in extra:
    yy = para(d, ax + 28, yy, "\u2022  " + item, sans(15), pw - 42, gap=18)
    yy += 6

# ---- footer ---------------------------------------------------------------
d.rectangle([24, 914, W - 24, 916], fill=GREY)
d.text((512, 926), "Six stories, one day  •  As reported 25 Nov 2026  •  "
       "Reuters · AP", font=sans(16), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
