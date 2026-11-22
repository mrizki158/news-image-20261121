"""Build the news-image-20261121 front page (1024x1024 PNG).

A dense broadsheet for the FULL day of Saturday 21 November 2026, on
the house layout proven by news-image-20261120: masthead naming the
day and its top stories, four illustrated leads (scenes drawn fresh
with Pillow in this session -- every word on the page is typeset by
Pillow so nothing can garble), ten small tiles with drawn pictograms,
a markets strip, a pinned dot-matrix world map beside a 31-item world
index, a "Saturday in five acts" strip and a sources/date-check
footer. 45 sourced stories in total.

Every story was cross-checked against at least two independent
reports dated 21 November 2026 before it was drawn; the market
figures were verified against WSJ and Reuters. The Riemann item is
framed as a claim, as reported. No event times are shown anywhere:
precise UTC times for the day were not verifiable, so the day is
told in five acts instead of on a clock.

Deterministic: no clock, no unseeded randomness, no network. Run
twice and the bytes are identical. Any text that does not fit its
allotted lines is counted in OVERFLOWS and printed at the end; the
target is zero.
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 14                       # outer margin
CW = W - 2 * M               # content width

PAPER = (247, 243, 234)
INK = (20, 20, 18)
SOFT = (74, 74, 68)
RULE = (160, 155, 145)
RED = (164, 31, 31)
NAVY = (28, 58, 94)
NAVY_BAND = (24, 48, 80)
AMBER = (198, 132, 26)
FAINT = (232, 228, 218)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 17)
F_SUB = font("DejaVuSans.ttf", 11)
F_KICK = font("DejaVuSans-Bold.ttf", 10)
F_HEAD = font("DejaVuSerif-Bold.ttf", 15)
F_STAND = font("DejaVuSans.ttf", 11)
F_TILE_H = font("DejaVuSans-Bold.ttf", 11)
F_TILE_F = font("DejaVuSans.ttf", 10)
F_SEC = font("DejaVuSans-Bold.ttf", 12)
F_IDX = font("DejaVuSans.ttf", 10)
F_IDX_B = font("DejaVuSans-Bold.ttf", 10)
F_SMALL = font("DejaVuSans.ttf", 9)
F_MARKET = font("DejaVuSans-Bold.ttf", 12)
F_TIME = font("DejaVuSans-Bold.ttf", 9)
F_TL = font("DejaVuSans.ttf", 9)

OVERFLOWS = []


# ------------------------------------------------------------------ stories
# (kicker, headline, standfirst, scene kind) -- the day's four leads.
LEADS = [
    ("MANAMA \u2014 THE GULF",
     "Iran says it struck US bases in Bahrain",
     "Iran claims two US bases hit; Bahrain reports an industrial "
     "fire, no injuries.",
     "manama"),
    ("NEW YORK \u2014 MARKETS",
     "AI rout puts S&P, Dow in correction",
     "S&P \u22123.7% in a 7th straight loss; Nasdaq \u22125.3%; Nvidia "
     "\u221214%; bitcoin under $60,000.",
     "markets"),
    ("KRYVYI RIH \u2014 UKRAINE",
     "Russian missile hits Zelensky\u2019s hometown",
     "Ballistic strike kills 2 and wounds 58 in the president\u2019s "
     "home city.",
     "kryvyi"),
    ("SINALOA \u2014 MEXICO",
     "Cartel boss \u201cChapo Isidro\u201d captured",
     "FBI most-wanted boss seized in Guasave; at least 11 die in "
     "the aftermath.",
     "sinaloa"),
]

# (section, headline, fact line, pictogram kind)
TILES = [
    ("CLIMATE", "COP31 deadlocked in overtime",
     "Fossil-fuel text still disputed.", "leaf"),
    ("JUSTICE", "France to take ICJ ruling to UN",
     "Security Council meeting sought.", "scales"),
    ("UKRAINE", "Zelensky: Putin \u201ca killer\u201d",
     "Trump defends his Putin ties.", "talks"),
    ("BALTIC", "Drones set Sparta II ablaze",
     "In the Gulf of Finland.", "ship"),
    ("GAZA", "Strike kills 3 in food vehicle",
     "Israeli strike hits aid route.", "truck"),
    ("RED SEA", "Houthis, Saudis trade strikes",
     "71 strikes claimed in a day.", "blast"),
    ("SCIENCE", "Mathematician claims Riemann proof",
     "AI-assisted claim by Alp\u00f6ge.", "graph"),
    ("WASHINGTON", "FBI crime database hacked",
     "NCIC breach reported.", "cyber"),
    ("SPACE", "BepiColombo reaches Mercury",
     "Orbit after an 8-year cruise.", "orbit"),
    ("SPORT", "England rout the All Blacks",
     "37\u201312, a record margin.", "rugby"),
]

# 31 more stories: (bold lead-in, rest of headline)
INDEX = [
    ("UK\u2013EU:", "sign three post-Brexit deals"),
    ("EU\u2013Indonesia:", "trade deal signed; 98.5% of tariffs cut"),
    ("EU budget:", "Costa proposes \u20ac1.78tn, 3% Big Tech tax"),
    ("Trump:", "threatens tax on firms building data centers abroad"),
    ("UN:", "talks keep working on AI-weapons rules"),
    ("Denmark:", "expels Russian diplomat over alleged plot"),
    ("France:", "cost-of-living protests; 144 arrested"),
    ("Zecler case:", "Paris officers sentenced for racist beating"),
    ("Los Angeles:", "Palisades-fire arson conviction"),
    ("Brazil:", "Bolsonaro in intensive care"),
    ("Haiti:", "Salvadoran troops battle gangs"),
    ("Nigeria:", "funeral boat capsizes; 24 dead"),
    ("Saudi\u2013Japan:", "deal triples oil stockpile to 24M barrels"),
    ("New York:", "Nikhil Gupta gets 20 years in Sikh murder plot"),
    ("Basra:", "power-station fire kills 4, injures 35"),
    ("Peru:", "magnitude 6.7 earthquake strikes"),
    ("Paris:", "Depardieu\u2013Houellebecq investigation opened"),
    ("Texas:", "inmate cried out in hour-long execution"),
    ("Villepin:", "announces French presidential run"),
    ("South Africa:", "Mlambo-Ngcuka dies at 71"),
    ("Estonia:", "to close Russia border crossings Dec 1"),
    ("Japan:", "felt sidelined at Shenzhen summit"),
    ("ATP Finals:", "Alcaraz to face Zverev in the final"),
    ("Las Vegas:", "Verstappen on pole"),
    ("Kane:", "out for months with torn ankle ligament"),
    ("Harden:", "scores 51, passes Kobe\u2019s 50-point mark"),
    ("Cincinnati:", "Fiona the hippo dies"),
    ("Hormuz:", "Lewis Pugh swims the strait"),
    ("Iraq:", "joint-presence deal with Kata\u2019ib Hezbollah"),
    ("LPGA:", "A Lim Kim leads finale after a hole-in-one"),
    ("Rugby:", "Wallabies beat Wales 29\u201326"),
]

# The day in five acts (no clock times: none were verifiable).
ACTS = [
    ("ACT I \u00b7 THE GULF", "Iran strikes US bases in Bahrain"),
    ("ACT II \u00b7 THE WAR", "Missile kills 2 in Kryvyi Rih"),
    ("ACT III \u00b7 MARKETS", "AI rout: S&P, Dow in correction"),
    ("ACT IV \u00b7 THE LAW", "\u201cChapo Isidro\u201d held in Sinaloa"),
    ("ACT V \u00b7 THE PLAY", "England rout All Blacks 37\u201312"),
]

MARKETS = ("MARKETS  \u00b7  S&P 500 \u22123.7% to 6,910  \u00b7  Dow \u2212949  "
           "\u00b7  Nasdaq \u22125.3%  \u00b7  Nvidia \u221214% to $125.53  "
           "\u00b7  Bitcoin under $60k  \u00b7  Brent $90")

# Lead pins (number, lon, lat): Manama, New York, Kryvyi Rih, Sinaloa.
PINS = [(1, 50, 26), (2, -74, 41), (3, 33, 48), (4, -108, 26)]
DOTS = [(31, 37), (2, 49), (27, 60), (34, 31), (44, 15), (0, 51),
        (107, -6), (12, 56), (-72, 19), (8, 10), (139, 36), (-75, -9),
        (25, 59), (8, 45), (-115, 36), (44, 33), (151, -34), (-84, 39)]

# Coarse continent outlines (lon, lat) for the dot-matrix map, drawn
# from a world atlas by hand; the dot grid at 8 px spacing only needs
# recognisable shapes.
LAND = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 73),
     (-100, 73), (-90, 73), (-85, 70), (-80, 73), (-75, 72), (-65, 60),
     (-60, 55), (-55, 47), (-60, 45), (-70, 42), (-75, 35), (-80, 32),
     (-81, 26), (-84, 30), (-90, 29), (-97, 26), (-97, 16), (-94, 17),
     (-92, 15), (-86, 13), (-83, 9), (-79, 9), (-83, 15), (-90, 14),
     (-95, 16), (-105, 20), (-110, 23), (-114, 29), (-120, 34),
     (-124, 40), (-124, 48), (-130, 55), (-140, 60), (-150, 60),
     (-158, 58), (-165, 60)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-65, -25), (-58, -27), (-52, -33), (-48, -28),
     (-40, -22), (-35, -9), (-35, -6), (-40, -3), (-50, 0), (-55, 5),
     (-60, 8), (-68, 11), (-72, 12), (-77, 7)],
    # Africa
    [(-6, 35), (-10, 31), (-15, 27), (-17, 15), (-15, 11), (-12, 8),
     (-8, 5), (-4, 5), (6, 4), (9, 4), (13, -1), (12, -6), (13, -12),
     (12, -18), (14, -22), (16, -28), (20, -35), (26, -34), (32, -29),
     (35, -24), (40, -15), (42, -11), (46, -1), (51, 2), (51, 11),
     (48, 11), (44, 12), (40, 15), (38, 18), (37, 22), (34, 28),
     (32, 31), (25, 32), (19, 33), (11, 34), (10, 37), (0, 36)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49),
     (0, 50), (3, 51), (5, 53), (8, 57), (10, 59), (5, 60), (5, 62),
     (12, 65), (18, 69), (25, 71), (30, 70), (32, 68), (28, 66),
     (24, 60), (21, 55), (19, 54), (15, 54), (12, 54), (8, 55),
     (8, 57), (3, 58), (-2, 57), (-5, 50), (-8, 43), (-9, 37)],
    # Asia: north coast eastward, down the Pacific side, around
    # South-East Asia, India and Arabia, back to Turkey.
    [(30, 36), (28, 44), (32, 48), (36, 52), (40, 56), (45, 60),
     (50, 63), (58, 66), (66, 68), (74, 71), (82, 73), (90, 75),
     (98, 76), (106, 76), (114, 74), (122, 72), (130, 71), (138, 71),
     (146, 71), (154, 69), (162, 67), (170, 66), (178, 65), (172, 62),
     (166, 60), (162, 57), (158, 53), (156, 51), (150, 59), (142, 59),
     (141, 50), (140, 44), (139, 39), (136, 35), (133, 34), (130, 31),
     (127, 34), (126, 38), (122, 39), (120, 35), (121, 31), (120, 27),
     (118, 25), (114, 22), (110, 20), (108, 18), (106, 10), (104, 9),
     (103, 7), (100, 8), (99, 11), (98, 14), (96, 16), (94, 17),
     (92, 21), (91, 22), (89, 22), (87, 18), (86, 20), (84, 19),
     (82, 17), (80, 15), (80, 13), (79, 10), (77, 8), (76, 10),
     (74, 15), (72, 20), (70, 21), (68, 23), (66, 25), (64, 25),
     (61, 25), (58, 25), (57, 26), (55, 27), (52, 28), (50, 29),
     (48, 30), (46, 29), (44, 29), (42, 29), (40, 30), (38, 31),
     (36, 33), (35, 31), (34, 31), (33, 31), (31, 32), (30, 34)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (141, 41), (143, 42), (145, 44)],
    # South-East Asian islands
    [(95, 5), (98, 3), (100, 0), (102, -3), (105, -5), (108, -7),
     (111, -7), (114, -8), (117, -9), (120, -10), (123, -10), (126, -9),
     (129, -4), (131, -2), (134, -3), (136, -4), (138, -6), (141, -8)],
    # Australia
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (170, -42), (173, -40), (176, -38), (178, -38)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
     (1, 51), (-2, 50)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (50, -20), (47, -25), (44, -25),
     (43, -20)],
]


# ------------------------------------------------------------------ helpers
def wrap_text(text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def take(lines, limit, what):
    """Keep at most `limit` lines; record an overflow if lines are cut."""
    if len(lines) > limit:
        OVERFLOWS.append("%s: %d lines, kept %d" % (what, len(lines), limit))
    return lines[:limit]


def point_in_poly(x, y, poly):
    """Ray-casting point-in-polygon test."""
    hit = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < xin:
                hit = not hit
    return hit


def is_land(lon, lat):
    return any(point_in_poly(lon, lat, poly) for poly in LAND)


def vgrad(w, h, top, bottom):
    """A vertical colour gradient as an RGB image."""
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t)
                         for i in range(3))
    return strip.resize((w, h))


# ------------------------------------------------------- lead scene painters
PW, PH = 243, 128          # lead panel size


def scene_manama():
    """Bahrain harbour at dusk: skyline, an industrial fire, the sea."""
    img = vgrad(PW, PH, (52, 44, 82), (216, 112, 62))
    d = ImageDraw.Draw(img)
    d.ellipse([150, 58, 178, 86], fill=(244, 178, 96))          # low sun
    sil = (30, 25, 42)
    # skyline: plain towers, then the twin pointed trade-centre towers
    for x, wdt, top in ((6, 16, 52), (26, 12, 62), (44, 18, 46),
                        (150, 14, 56), (196, 12, 60), (228, 12, 54)):
        d.rectangle([x, top, x + wdt, 88], fill=sil)
    for cx in (88, 122):                                        # twin towers
        d.polygon([(cx - 13, 88), (cx - 6, 30), (cx, 18),
                   (cx + 6, 30), (cx + 13, 88)], fill=sil)
    d.rectangle([0, 86, PW, 90], fill=sil)                       # quay
    # industrial site, right: tanks, a flame and a smoke plume
    for x in (168, 190, 212):
        d.rounded_rectangle([x, 70, x + 18, 88], radius=4, fill=sil)
    d.ellipse([196, 58, 208, 72], fill=(240, 120, 40))
    d.ellipse([199, 62, 205, 70], fill=(250, 190, 80))
    for i, (cx, cy, r) in enumerate(((206, 48, 7), (214, 38, 9),
                                     (224, 28, 11), (234, 20, 8))):
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                  fill=(96, 88, 92))
    # sea with dusk reflections
    d.rectangle([0, 90, PW, PH], fill=(23, 31, 53))
    rng = random.Random(11)
    for _ in range(46):
        x = rng.randrange(2, PW - 22)
        y = rng.randrange(94, PH - 3)
        ln = rng.randrange(6, 20)
        col = (214, 140, 84) if rng.random() < 0.4 else (90, 104, 138)
        d.line([x, y, x + ln, y], fill=col, width=1)
    return img


def scene_markets():
    """A trading screen in the red: a falling chart and candlesticks."""
    img = Image.new("RGB", (PW, PH), (14, 18, 32))
    d = ImageDraw.Draw(img)
    for gx in range(12, PW, 24):                                # grid
        d.line([gx, 8, gx, PH - 8], fill=(30, 38, 58), width=1)
    for gy in range(10, PH, 20):
        d.line([8, gy, PW - 8, gy], fill=(30, 38, 58), width=1)
    pts = [(14, 26), (44, 34), (66, 30), (92, 48), (118, 44),
           (142, 62), (168, 58), (196, 78), (228, 92)]
    d.line(pts, fill=(110, 20, 20), width=6)
    d.line(pts, fill=(232, 52, 44), width=3)
    x, y = pts[-1]
    d.polygon([(x - 2, y - 8), (x + 10, y + 2), (x - 8, y + 4)],
              fill=(232, 52, 44))
    rng = random.Random(5)
    base = 108                                                  # candles
    for i in range(9):
        cx = 16 + i * 25
        top = base - 26 - i * 2 + rng.randrange(0, 5)
        d.rectangle([cx, top, cx + 13, base - 4], fill=(196, 40, 36))
        d.line([cx + 6, top - 5, cx + 6, base + 1], fill=(196, 40, 36),
               width=2)
    for i in range(5):                                          # ticker blocks
        col = (196, 40, 36) if i % 2 == 0 else (52, 140, 74)
        d.rectangle([168 + (i % 3) * 24, 10 + (i // 3) * 14,
                     186 + (i % 3) * 24, 19 + (i // 3) * 14], fill=col)
    return img


def scene_kryvyi():
    """Night strike on a housing block: burst, streak, lit windows."""
    img = vgrad(PW, PH, (10, 12, 26), (38, 34, 48))
    d = ImageDraw.Draw(img)
    rng = random.Random(23)
    for _ in range(26):                                         # stars
        x, y = rng.randrange(0, PW), rng.randrange(0, 46)
        d.point((x, y), fill=(170, 176, 200))
    blocks = [(8, 44, 52, 96), (58, 56, 92, 96), (98, 38, 140, 96),
              (196, 52, 234, 96)]
    for (x0, y0, x1, y1) in blocks:                             # blocks
        d.rectangle([x0, y0, x1, y1], fill=(20, 22, 36))
    rng = random.Random(31)
    for (x0, y0, x1, y1) in blocks:                             # windows
        for wy in range(y0 + 6, y1 - 6, 9):
            for wx in range(x0 + 5, x1 - 5, 8):
                if rng.random() < 0.42:
                    d.rectangle([wx, wy, wx + 4, wy + 5],
                                fill=(238, 186, 96))
    d.line([16, 6, 168, 66], fill=(250, 214, 150), width=3)     # streak
    d.line([16, 6, 168, 66], fill=(255, 244, 214), width=1)
    import math
    cx, cy = 172, 70                                            # burst
    for ang in range(0, 360, 24):
        a = math.radians(ang)
        d.line([cx, cy, cx + 26 * math.cos(a), cy + 20 * math.sin(a)],
               fill=(240, 120, 40), width=3)
    d.ellipse([cx - 11, cy - 9, cx + 11, cy + 9], fill=(246, 150, 52))
    d.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=(252, 208, 110))
    for i, (sx, sy, r) in enumerate(((186, 52, 8), (198, 40, 10),
                                     (210, 30, 8))):           # smoke
        d.ellipse([sx - r, sy - r // 2, sx + r, sy + r // 2],
                  fill=(88, 82, 90))
    d.rectangle([0, 96, PW, PH], fill=(13, 14, 22))             # street
    d.ellipse([30, 104, 36, 108], fill=(70, 120, 250))          # blue light
    d.ellipse([42, 104, 48, 108], fill=(232, 52, 44))           # red light
    d.ellipse([206, 104, 212, 108], fill=(70, 120, 250))
    return img


def scene_sinaloa():
    """Dawn raid in Sinaloa: sun over hills, a convoy on the road."""
    img = vgrad(PW, PH, (34, 38, 76), (240, 164, 84))
    d = ImageDraw.Draw(img)
    d.ellipse([96, 52, 140, 96], fill=(250, 196, 104))          # rising sun
    d.polygon([(0, 78), (60, 58), (130, 74), (190, 56), (243, 72),
               (243, 128), (0, 128)], fill=(74, 48, 52))        # far hills
    d.polygon([(0, 96), (70, 82), (150, 94), (243, 84), (243, 128),
               (0, 128)], fill=(40, 28, 34))                    # near hills
    d.polygon([(104, 128), (134, 128), (126, 96), (114, 96)],
              fill=(24, 20, 24))                                # road
    for i, (cx, cy, wdt) in enumerate(((118, 116, 17), (120, 105, 12),
                                       (121, 98, 8))):          # convoy
        d.rectangle([cx - wdt // 2, cy - 5, cx + wdt // 2, cy + 2],
                    fill=(10, 10, 12))
        d.rectangle([cx - wdt // 4, cy - 8, cx + wdt // 4, cy - 5],
                    fill=(10, 10, 12))
        d.point((cx - wdt // 3, cy), fill=(250, 220, 150))
        d.point((cx + wdt // 3, cy), fill=(250, 220, 150))
    hx, hy = 196, 26                                            # helicopter
    d.ellipse([hx - 13, hy - 5, hx + 13, hy + 5], fill=(16, 14, 18))
    d.line([hx - 20, hy - 9, hx + 20, hy - 9], fill=(16, 14, 18), width=2)
    d.polygon([(hx + 10, hy - 2), (hx + 26, hy - 6), (hx + 26, hy - 2),
               (hx + 10, hy + 2)], fill=(16, 14, 18))
    d.line([hx + 26, hy - 8, hx + 26, hy], fill=(16, 14, 18), width=2)
    return img


SCENES = {"manama": scene_manama, "markets": scene_markets,
          "kryvyi": scene_kryvyi, "sinaloa": scene_sinaloa}


def draw_mini(d, box, kind):
    """Draw a small pictogram inside box (x0, y0, x1, y1)."""
    import math
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "orbit":
        d.ellipse([cx - 22, cy - 14, cx + 22, cy + 14], outline=NAVY, width=2)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        d.ellipse([cx + 16, cy - 12, cx + 22, cy - 6], fill=AMBER)
    elif kind == "ship":
        d.polygon([(cx - 20, cy + 2), (cx + 20, cy + 2), (cx + 12, cy + 12),
                   (cx - 12, cy + 12)], fill=NAVY)
        d.rectangle([cx - 6, cy - 12, cx + 2, cy + 2], fill=NAVY)
        d.line([cx + 2, cy - 12, cx + 14, cy - 2], fill=RED, width=2)
        d.ellipse([cx + 8, cy - 12, cx + 16, cy - 4], fill=AMBER)
    elif kind == "talks":
        d.rounded_rectangle([x0 + 10, y0 + 6, cx + 6, cy + 8], radius=6,
                            outline=NAVY, width=2)
        d.rounded_rectangle([cx - 6, cy - 4, x1 - 10, y1 - 8], radius=6,
                            outline=RED, width=2)
        d.line([x0 + 16, y0 + 12, cx, y0 + 12], fill=NAVY, width=2)
        d.line([cx, y1 - 14, x1 - 16, y1 - 14], fill=RED, width=2)
    elif kind == "blast":
        for ang in range(0, 360, 30):
            r1, r2 = 6, 20
            a = math.radians(ang)
            d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                    cx + r2 * math.cos(a), cy + r2 * math.sin(a)],
                   fill=RED, width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=AMBER)
    elif kind == "leaf":
        d.ellipse([cx - 16, cy - 12, cx + 16, cy + 12], outline=NAVY, width=2)
        d.line([cx - 14, cy + 10, cx + 14, cy - 10], fill=NAVY, width=2)
        for dx, dy in ((-8, -2), (0, -6), (8, -2)):
            d.line([cx + dx, cy + dy, cx + dx - 5, cy + dy - 6],
                   fill=NAVY, width=1)
    elif kind == "cyber":
        d.rectangle([x0 + 12, y0 + 6, x1 - 12, y1 - 6], outline=NAVY, width=2)
        d.line([x0 + 12, y0 + 14, x1 - 12, y0 + 14], fill=NAVY, width=1)
        d.ellipse([x0 + 16, y0 + 9, x0 + 19, y0 + 12], fill=RED)
        d.polygon([(cx + 3, cy - 10), (cx - 5, cy + 1), (cx - 1, cy + 1),
                   (cx - 3, cy + 10), (cx + 5, cy - 1), (cx + 1, cy - 1)],
                  fill=RED)
    elif kind == "scales":
        d.line([cx, y0 + 6, cx, y1 - 8], fill=NAVY, width=2)
        d.line([cx - 18, y0 + 10, cx + 18, y0 + 10], fill=NAVY, width=2)
        d.ellipse([cx - 3, y0 + 3, cx + 3, y0 + 9], fill=RED)
        for sx in (cx - 18, cx + 18):
            d.line([sx, y0 + 10, sx - 6, y0 + 22], fill=NAVY, width=1)
            d.line([sx, y0 + 10, sx + 6, y0 + 22], fill=NAVY, width=1)
            d.arc([sx - 8, y0 + 18, sx + 8, y0 + 30], start=0, end=180,
                  fill=NAVY, width=2)
        d.rectangle([cx - 10, y1 - 8, cx + 10, y1 - 5], fill=NAVY)
    elif kind == "truck":
        d.rectangle([x0 + 8, cy - 12, cx + 8, cy + 8], outline=NAVY, width=2)
        d.polygon([(cx + 8, cy - 4), (cx + 20, cy - 4), (cx + 24, cy + 2),
                   (cx + 24, cy + 8), (cx + 8, cy + 8)], fill=NAVY)
        d.rectangle([cx + 12, cy - 2, cx + 19, cy + 3], fill=PAPER)
        for wx in (x0 + 18, cx - 2, cx + 17):
            d.ellipse([wx - 4, cy + 5, wx + 4, cy + 13], fill=INK)
        d.line([x0 + 8, cy + 12, x1 - 8, cy + 12], fill=RULE, width=1)
        d.line([x0 + 14, cy - 6, cx + 2, cy - 6], fill=RED, width=2)
    elif kind == "graph":
        d.line([x0 + 10, y0 + 6, x0 + 10, y1 - 6], fill=NAVY, width=2)
        d.line([x0 + 10, y1 - 6, x1 - 8, y1 - 6], fill=NAVY, width=2)
        pts = [(x0 + 14, y1 - 10), (x0 + 26, y1 - 16), (x0 + 36, y1 - 13),
               (x0 + 48, y1 - 24), (x0 + 60, y1 - 20), (x1 - 14, y0 + 10)]
        d.line(pts, fill=RED, width=2)
        for (px, py) in pts[1:-1]:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    elif kind == "rugby":
        d.ellipse([cx - 22, cy - 12, cx + 22, cy + 12], outline=INK, width=2)
        d.arc([cx - 12, cy - 12, cx + 4, cy + 12], start=90, end=270,
              fill=INK, width=1)
        d.arc([cx - 4, cy - 12, cx + 12, cy + 12], start=270, end=90,
              fill=INK, width=1)
        for dx in (-4, 0, 4):
            d.line([cx + dx, cy - 3, cx + dx, cy + 3], fill=RED, width=2)


# ------------------------------------------------------------------ sections
def draw_masthead(d):
    d.text((M, 6), "THE WORLD TODAY", font=F_MAST, fill=INK)
    date = "SATURDAY 21 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text((W - M - dw, 12), date, font=F_DATE, fill=INK)
    sub = "45 SOURCED STORIES"
    sw = d.textlength(sub, font=F_KICK)
    d.text((W - M - sw, 36), sub, font=F_KICK, fill=RED)
    d.line([M, 68, W - M, 68], fill=INK, width=2)
    d.text((M, 74), "Iran strikes Bahrain bases \u00b7 AI rout sinks "
           "the S&P \u00b7 Missile hits Zelensky\u2019s hometown",
           font=F_SUB, fill=SOFT)
    right = "FULL-DAY EDITION \u00b7 v1"
    rw = d.textlength(right, font=F_SUB)
    d.text((W - M - rw, 74), right, font=F_SUB, fill=SOFT)


def draw_leads(d, img):
    y = 94
    colw = 243
    gap = 8
    for i, (kicker, head, stand, kind) in enumerate(LEADS):
        x = M + i * (colw + gap)
        img.paste(SCENES[kind](), (x, y))
        d.rectangle([x, y, x + colw - 1, y + 127], outline=RULE, width=1)
        ty = y + 134
        d.text((x, ty), kicker, font=F_KICK, fill=RED)
        ty += 14
        for line in take(wrap_text(head, F_HEAD, colw), 3,
                         "lead %d headline" % (i + 1)):
            d.text((x, ty), line, font=F_HEAD, fill=INK)
            ty += 18
        ty += 2
        for line in take(wrap_text(stand, F_STAND, colw), 3,
                         "lead %d standfirst" % (i + 1)):
            d.text((x, ty), line, font=F_STAND, fill=SOFT)
            ty += 13


def draw_tiles(d):
    d.text((M, 340), "MORE OF THE DAY", font=F_SEC, fill=INK)
    d.line([M + 150, 348, W - M, 348], fill=RULE, width=1)
    tw, th = 192, 112
    gapx, gapy = 8, 6
    x0, y0 = 16, 358
    for i, (sec, head, fact, kind) in enumerate(TILES):
        col, row = i % 5, i // 5
        x = x0 + col * (tw + gapx)
        y = y0 + row * (th + gapy)
        d.rectangle([x, y, x + tw - 1, y + th - 1], outline=RULE, width=1)
        draw_mini(d, (x + 4, y + 4, x + tw - 4, y + 42), kind)
        d.line([x + 4, y + 46, x + tw - 4, y + 46], fill=FAINT, width=1)
        ty = y + 50
        d.text((x + 6, ty), sec, font=F_KICK, fill=RED)
        ty += 13
        for line in take(wrap_text(head, F_TILE_H, tw - 12), 2,
                         "tile %d headline" % (i + 1)):
            d.text((x + 6, ty), line, font=F_TILE_H, fill=INK)
            ty += 13
        for line in take(wrap_text(fact, F_TILE_F, tw - 12), 1,
                         "tile %d fact" % (i + 1)):
            d.text((x + 6, ty), line, font=F_TILE_F, fill=SOFT)
            ty += 12


def draw_markets(d):
    y = 594
    d.rectangle([M, y, W - M - 1, y + 26], fill=NAVY_BAND)
    fnt = F_MARKET
    tw = d.textlength(MARKETS, font=fnt)
    if tw > CW - 16:
        fnt = font("DejaVuSans-Bold.ttf", 11)
        tw = d.textlength(MARKETS, font=fnt)
    if tw > CW - 16:
        OVERFLOWS.append("markets strip too wide: %d px" % tw)
    d.text(((W - tw) / 2, y + 7), MARKETS, font=fnt, fill=(255, 255, 255))


def draw_map(d, x0, y0, w, h):
    d.text((x0, y0), "WHERE IT HAPPENED", font=F_SEC, fill=INK)
    mx, my = x0, y0 + 22
    mw, mh = w, h - 40
    step = 8
    gx, gy = mx + 4, my + 4
    while gy < my + mh - 4:
        lon = (gx - mx) / mw * 360 - 180
        lat = 90 - (gy - my) / mh * 180
        if is_land(lon, lat):
            d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=NAVY)
        gy += step
        if gy >= my + mh - 4:
            gy = my + 4
            gx += step
            if gx >= mx + mw - 4:
                break
    for lon, lat in DOTS:
        px = mx + (lon + 180) / 360 * mw
        py = my + (90 - lat) / 180 * mh
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=AMBER,
                  outline=(255, 255, 255), width=1)
    for num, lon, lat in PINS:
        px = mx + (lon + 180) / 360 * mw
        py = my + (90 - lat) / 180 * mh
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(str(num), font=F_TIME)
        d.text((px - tw / 2, py - 5), str(num), font=F_TIME,
               fill=(255, 255, 255))
    d.text((x0, y0 + h - 16),
           "Red pins: the four lead stories. Amber dots: the rest of the day.",
           font=F_SMALL, fill=SOFT)


def draw_index(d, x0, y0):
    d.text((x0, y0), "THE WORLD IN BRIEF \u2014 31 MORE STORIES",
           font=F_SEC, fill=INK)
    cols = 3
    colw = 204
    gapx = 10
    rowh = 26
    iy = y0 + 22
    for i, (lead, rest) in enumerate(INDEX):
        col, row = i % cols, i // cols
        x = x0 + col * (colw + gapx)
        y = iy + row * rowh
        d.ellipse([x, y + 3, x + 6, y + 9], fill=RED)
        tx = x + 11
        full = lead + " " + rest
        lines = take(wrap_text(full, F_IDX, colw - 11), 2,
                     "index %d" % (i + 1))
        ty = y
        for li, line in enumerate(lines):
            if li == 0 and line.startswith(lead):
                d.text((tx, ty), lead, font=F_IDX_B, fill=INK)
                lw = d.textlength(lead, font=F_IDX_B)
                d.text((tx + lw, ty), line[len(lead):], font=F_IDX,
                       fill=INK)
            else:
                d.text((tx, ty), line, font=F_IDX, fill=INK)
            ty += 12


def draw_acts(d):
    y = 952
    d.text((M, y), "SATURDAY IN FIVE ACTS", font=F_SEC, fill=INK)
    d.text((M + 208, y + 2), "the day in five chapters, from the Gulf "
           "strikes to the rugby", font=F_SUB, fill=SOFT)
    cellw = CW // 5
    ty = y + 18
    for i, (kick, label) in enumerate(ACTS):
        x = M + i * cellw
        if i:
            d.line([x - 4, ty + 2, x - 4, ty + 22], fill=RULE, width=1)
        d.text((x, ty), kick, font=F_KICK, fill=RED)
        for line in take(wrap_text(label, F_TL, cellw - 10), 1,
                         "act %d" % (i + 1)):
            d.text((x, ty + 12), line, font=F_TL, fill=INK)


def draw_footer(d):
    d.line([M, 996, W - M, 996], fill=RULE, width=1)
    d.text((M, 1001),
           "Sources: Reuters \u00b7 WSJ \u00b7 BBC \u00b7 Al Jazeera \u00b7 "
           "Euronews \u00b7 France 24 \u00b7 UPI \u00b7 The Guardian \u00b7 "
           "CBS \u00b7 CBC \u2014 every story cross-checked against "
           "reports dated 21 Nov 2026.",
           font=F_SMALL, fill=SOFT)
    d.text((M, 1013),
           "Date check: today is Saturday 21 November 2026. Full-day "
           "edition \u2014 45 stories: the Bahrain strikes, the AI rout "
           "and the Kryvyi Rih missile lead the day.",
           font=F_SMALL, fill=SOFT)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_leads(d, img)
    draw_tiles(d)
    draw_markets(d)
    d.line([366, 628, 366, 946], fill=RULE, width=1)
    draw_map(d, M, 628, 340, 318)
    draw_index(d, 378, 628)
    draw_acts(d)
    draw_footer(d)
    return img


def main():
    img = build()
    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("entry.png:", img.size, size, "bytes")
    print("stories:", len(LEADS) + len(TILES) + len(INDEX))
    print("overflows:", len(OVERFLOWS))
    for o in OVERFLOWS:
        print("  OVERFLOW:", o)


if __name__ == "__main__":
    main()
