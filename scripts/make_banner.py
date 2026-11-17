"""Draws the profile banner, pixel-banner.svg: a coder's room at night.

Every element is drawn here from rectangles on a 256 x 144 grid; nothing is copied from
other artwork. Edit a colour in the palette or an item's section, then run:

    python scripts/make_banner.py            # rewrites pixel-banner.svg
    python scripts/make_banner.py --preview  # also writes preview.png (needs Pillow)

preview.png is a still, 5x scale image for checking your change; don't commit it.
"""
import argparse
import math
from pathlib import Path

W, H = 256, 144
REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- palette
C = dict(
    wall="#0b1026", brick="#111a3c", brick2="#0e1633", shadow="#080c1d",
    floor="#05081a", under="#0a0f24",
    pink="#ff3cd2", pinkhi="#ffc2f4", pinkglow="#3d1248", pinkmid="#a8248f",
    plaque="#e8619f", plaquehi="#ff9cc9", plaquedk="#9c2f68", ink="#3a0b2a",
    frame="#1d4f9c", framehi="#2f6fd0", sky="#0c1f4d", sky2="#132c66", moon="#f5efc4", moondk="#c9c08f",
    city="#081430", citywin="#ffd36b",
    wood="#6e4630", woodhi="#9a6644", wooddk="#3e2619",
    bezel="#1a2140", bezelhi="#2a3463", screen="#0d1530", screen2="#111c3d",
    c1="#ff79c6", c2="#8be9fd", c3="#50fa7b", c4="#f1fa8c", c5="#bd93f9", c6="#6272a4",
    green="#2fbf71", greendk="#1b7a48", greenhi="#7ee8a6", pot="#c0573a", potdk="#8a3a26",
    hair="#2b1520", hairhi="#4d2638", skin="#e8a989", skindk="#c07a62",
    hood="#6b3fa0", hoodhi="#8c5cc4", hooddk="#45276d", phones="#22d3c5", phonesdk="#128a80",
    chair="#1c2347", chairhi="#2c3768", metal="#596384",
    white="#e9ecf5", grey="#9aa3bd", greydk="#4a5373", black="#05070f",
    yellow="#ffd34d", orange="#ff9a3c", red="#ff4f5e", blue="#3a86ff", cyan="#36e2ff",
    mug="#e9ecf5", mugdk="#aab2cc", coffee="#4b2b1c",
    cat="#7d849c", catdk="#596078", cathi="#a3a9bd",
    lamp="#ffb347", lampdk="#c77a1f", book1="#e5484d", book2="#3a86ff", book3="#ffd34d", book4="#50c878",
)

layers = {}  # name -> {(x, y): colour}
order = []


def layer(name):
    if name not in layers:
        layers[name] = {}
        order.append(name)
    return layers[name]


cur = layer("base")


def use(name):
    global cur
    cur = layer(name)


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        cur[(x, y)] = C.get(c, c)


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(xx, yy, c)


def sprite(x, y, rows, key):
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch in key:
                px(x + dx, y + dy, key[ch])


FONT = {
    "A": ["010", "101", "111", "101", "101"], "B": ["110", "101", "110", "101", "110"],
    "D": ["110", "101", "101", "101", "110"], "E": ["111", "100", "110", "100", "111"],
    "H": ["101", "101", "111", "101", "101"], "I": ["111", "010", "010", "010", "111"],
    "K": ["101", "101", "110", "101", "101"], "L": ["100", "100", "100", "100", "111"],
    "P": ["110", "101", "110", "100", "100"], "Q": ["111", "101", "101", "111", "001"],
    "S": ["011", "100", "010", "001", "110"], "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"], "!": ["010", "010", "010", "000", "010"],
    " ": ["000", "000", "000", "000", "000"],
}


def text(x, y, s, c):
    for i, ch in enumerate(s):
        for dy, row in enumerate(FONT[ch]):
            for dx, bit in enumerate(row):
                if bit == "1":
                    px(x + i * 4 + dx, y + dy, c)


# ---------------------------------------------------------------- wall and floor
rect(0, 0, W, H, "wall")
# a soft diagonal shadow across the wall, like light from the window
for y in range(0, 104):
    x0 = 150 - y
    for x in range(max(0, x0 - 60), max(0, x0)):
        px(x, y, "shadow")
# scattered bricks
for bx, by in [(4, 6), (22, 12), (70, 4), (84, 10), (150, 8), (166, 14), (60, 40), (132, 50),
               (176, 46), (40, 70), (100, 52), (8, 88), (172, 92), (244, 72), (230, 96), (186, 64)]:
    rect(bx, by, 12, 4, "brick")
    rect(bx + 1, by + 1, 10, 2, "brick2")

# under the desk
rect(0, 112, W, 32, "under")
rect(0, 138, W, 6, "floor")

# ---------------------------------------------------------------- window (top right)
cx, cy, r = 222, 37, 27
for y in range(cy - r - 3, cy + r + 4):
    for x in range(cx - r - 3, cx + r + 4):
        d = math.hypot(x - cx + 0.5, y - cy + 0.5)
        if d <= r:
            px(x, y, "sky2" if y > cy + 6 else "sky")
        elif d <= r + 3:
            px(x, y, "frame" if d > r + 1 else "framehi")
# moon (crescent)
for y in range(cy - 20, cy - 4):
    for x in range(cx + 4, cx + 20):
        if math.hypot(x - (cx + 12), y - (cy - 12)) <= 7 and math.hypot(x - (cx + 15), y - (cy - 15)) > 6:
            px(x, y, "moon")
# skyline
for bx, bw, bh in [(198, 8, 10), (205, 6, 16), (211, 9, 12), (220, 7, 20), (227, 10, 13),
                   (237, 6, 17), (243, 8, 9)]:
    for y in range(cy + r - bh, cy + r + 1):
        for x in range(bx, bx + bw):
            if math.hypot(x - cx + 0.5, y - cy + 0.5) <= r:
                px(x, y, "city")
for wx, wy in [(207, 52), (209, 56), (222, 48), (224, 53), (229, 56), (239, 52), (213, 57)]:
    px(wx, wy, "citywin")
# window bars
rect(cx - 1, cy - r, 2, 2 * r + 1, "frame")
rect(cx - r, cy - 1, 2 * r + 1, 2, "frame")

# ---------------------------------------------------------------- hanging plant
rect(180, 0, 1, 16, "greydk")
rect(175, 16, 11, 2, "potdk")
rect(176, 18, 9, 5, "pot")
rect(177, 23, 7, 1, "potdk")
for vx, ln in [(175, 14), (178, 20), (181, 11), (184, 17), (186, 8)]:
    for i in range(ln):
        px(vx + (1 if (i // 3) % 2 else 0), 23 + i, "green" if i % 3 else "greendk")
        if i % 4 == 1:
            px(vx + 2, 23 + i, "greenhi")
rect(174, 14, 13, 2, "green")
rect(176, 13, 9, 1, "greenhi")

# ---------------------------------------------------------------- plaque with name (left)
rect(14, 54, 44, 15, "plaquedk")
rect(15, 55, 42, 13, "plaque")
rect(15, 55, 42, 1, "plaquehi")
text(20, 59, "SAKTHI Q", "ink")
rect(20, 69, 2, 3, "greydk")
rect(50, 69, 2, 3, "greydk")

# ---------------------------------------------------------------- poster (top centre)
rect(104, 8, 38, 40, "frame")
rect(106, 10, 34, 36, "#0f2350")
text(109, 13, "SHIP IT!", "c2")
rocket = [
    "....w....",
    "...www...",
    "..wwwww..",
    "..wbbbw..",
    "..wbcbw..",
    "..wbbbw..",
    "..wwwww..",
    ".pwwwwwp.",
    "pp.www.pp",
    "p..ooo..p",
    "...yoy...",
    "....y....",
]
sprite(118, 22, rocket, {"w": "white", "b": "blue", "c": "cyan", "p": "pink", "o": "orange", "y": "yellow"})
for sx, sy in [(109, 24), (135, 28), (111, 40), (133, 41), (126, 21)]:
    px(sx, sy, "c4")

# ---------------------------------------------------------------- sticky notes
rect(154, 50, 7, 7, "yellow")
rect(155, 52, 5, 1, "orange")
rect(155, 54, 4, 1, "orange")
rect(145, 49, 7, 7, "c1")
rect(146, 51, 5, 1, "#b83f87")
rect(146, 53, 3, 1, "#b83f87")

# ---------------------------------------------------------------- left shelf
rect(66, 62, 60, 2, "woodhi")
rect(66, 64, 60, 2, "wood")
rect(70, 66, 2, 4, "wooddk")
rect(120, 66, 2, 4, "wooddk")
# plant
rect(70, 55, 10, 7, "pot")
rect(70, 55, 10, 1, "potdk")
sprite(68, 44, [
    "....g.....g.",
    "...ggg...gg.",
    ".h.ggg..ggg.",
    "ggg.gg.ggh..",
    "gggg.gggg...",
    ".gggggggg..g",
    "..dggggggdgg",
    "...ddggggd..",
    "....dggdd...",
    "....ddddd...",
    ".....ddd....",
], {"g": "green", "d": "greendk", "h": "greenhi"})
# robot figurine (original)
sprite(84, 44, [
    "....c....",
    "....g....",
    ".ggggggg.",
    ".gwwwwwg.",
    ".gwcwcwg.",
    ".gwwwwwg.",
    ".ggggggg.",
    "...ggg...",
    "gggggggggg"[:9],
    "g.gpgpg.g",
    "g.ggggg.g",
    "..ggggg..",
    "..g...g..",
    ".gg...gg.",
    ".........",
    ".........",
    ".........",
    ".........",
], {"g": "grey", "w": "screen", "c": "cyan", "p": "pink"})
# books
for bx, bh, col in [(100, 12, "book1"), (104, 10, "book2"), (108, 13, "book3"), (112, 11, "book4")]:
    rect(bx, 62 - bh, 4, bh, col)
    rect(bx + 1, 62 - bh + 2, 2, 1, "white")
for i in range(11):  # a leaning book
    rect(117 + i // 3, 51 + i, 3, 1, "c5")

# ---------------------------------------------------------------- right shelf
rect(156, 76, 40, 2, "woodhi")
rect(156, 78, 40, 2, "wood")
rect(160, 80, 2, 4, "wooddk")
rect(190, 80, 2, 4, "wooddk")
# cactus
rect(159, 71, 8, 5, "pot")
rect(159, 71, 8, 1, "potdk")
rect(161, 61, 4, 10, "green")
rect(162, 61, 1, 10, "greenhi")
rect(158, 64, 2, 4, "green")
rect(166, 63, 2, 5, "green")
px(163, 60, "c1")
# trophy
sprite(171, 64, [
    "yyyyyyy",
    "yyyyyyy",
    "yyyyyyy",
    ".yyyyy.",
    "..yyy..",
    "...y...",
    "...y...",
    "..ooo..",
    ".ooooo.",
    ".ooooo.",
    ".ooooo.",
    ".ooooo.",
], {"y": "yellow", "o": "lampdk"})
px(169, 65, "yellow"); px(169, 66, "yellow"); px(178, 65, "yellow"); px(178, 66, "yellow")
# rubber duck
sprite(182, 68, [
    ".yyy....",
    "yyyyo...",
    "yyyy....",
    ".yyyyyy.",
    "yyyyyyyy",
    "yyyyyyyy",
    ".yyyyyy.",
    "........",
], {"y": "yellow", "o": "orange"})
px(183, 69, "black")

# ---------------------------------------------------------------- desk
rect(0, 104, W, 1, "woodhi")
rect(0, 105, W, 4, "wood")
rect(0, 109, W, 3, "wooddk")

# desk lamp (left)
rect(6, 101, 14, 3, "greydk")
for i in range(18):
    rect(11 + i // 2, 100 - i, 2, 1, "grey")
for i in range(8):
    rect(20 + i, 82 - i // 3, 2, 1, "grey")
sprite(26, 77, [
    "..lll...",
    ".lllll..",
    "lllllll.",
    "lllllll.",
    ".yyyyy..",
], {"l": "lamp", "y": "yellow"})

# side monitor (terminal)
rect(36, 74, 40, 27, "bezel")
rect(37, 75, 38, 1, "bezelhi")
rect(38, 77, 36, 22, "black")
term = [("$ ", "c3", 10), ("> ", "grey", 16), ("> ", "grey", 12), ("$ ", "c3", 14), ("OK", "c3", 6)]
for i, (_, col, ln) in enumerate(term):
    rect(40, 79 + i * 4, 2, 1, "c3" if i in (0, 3) else "greydk")
    rect(44, 79 + i * 4, ln, 1, col)
rect(53, 101, 6, 3, "bezel")
rect(48, 103, 16, 1, "bezelhi")

# main monitor (code editor)
mx, my, mw, mh = 84, 60, 70, 41
rect(mx, my, mw, mh, "bezel")
rect(mx + 1, my + 1, mw - 2, 1, "bezelhi")
rect(mx + 2, my + 3, mw - 4, mh - 5, "screen")
rect(mx + 2, my + 3, mw - 4, 3, "screen2")
px(mx + 4, my + 4, "red"); px(mx + 6, my + 4, "yellow"); px(mx + 8, my + 4, "c3")
rect(mx + 2, my + 6, 8, mh - 8, "screen2")  # line-number gutter
code = [
    [(0, 5, "c1"), (6, 9, "c2"), (16, 4, "white")],
    [(3, 6, "c5"), (10, 12, "c4")],
    [(3, 4, "c1"), (8, 7, "c2"), (16, 10, "c3")],
    [(6, 14, "white"), (21, 6, "c4")],
    [(6, 5, "c1"), (12, 16, "c3")],
    [(3, 3, "c6"), (7, 18, "c6")],
    [(3, 7, "c5"), (11, 5, "c2"), (17, 9, "c4")],
    [(0, 2, "white")],
]
for i, parts in enumerate(code):
    yy = my + 9 + i * 4
    rect(mx + 4, yy, 3, 1, "c6")
    for ox, ln, col in parts:
        rect(mx + 12 + ox, yy, ln, 1, col)
rect(116, 101, 8, 3, "bezel")
rect(108, 103, 24, 1, "bezelhi")

# keyboard and mouse
rect(96, 101, 36, 3, "greydk")
for kx in range(97, 131, 2):
    px(kx, 102, "grey")
rect(137, 102, 4, 2, "grey")

# mug (right)
rect(176, 94, 9, 10, "mug")
rect(176, 94, 9, 1, "mugdk")
rect(177, 95, 7, 1, "coffee")
rect(185, 96, 2, 1, "mug"); rect(186, 97, 1, 3, "mug"); rect(185, 100, 2, 1, "mug")
rect(178, 98, 5, 2, "c1")

# speaker
rect(194, 86, 11, 18, "bezel")
rect(195, 87, 9, 1, "bezelhi")
for sy, rr in [(92, 2), (99, 3)]:
    for y in range(sy - rr, sy + rr + 1):
        for x in range(199 - rr, 200 + rr):
            if math.hypot(x - 199.5 + 0.5, y - sy) <= rr:
                px(x, y, "greydk")
    px(199, sy, "black")

# sleeping cat (original)
sprite(212, 92, [
    "..k...k.............",
    ".kkk.kkk............",
    ".kkkkkkk.......tt...",
    "kkkkkkkkkkkkk...tt..",
    "kcckkcckkkkkkkk..t..",
    "kkkkkkkkkkkkkkkk.t..",
    ".kkkhkkkkkkkkkkkt...",
    ".kkkkkkkkkkkkkkkt...",
    "..dddkkkkkkkkkkt....",
    "...dddddddddddd.....",
    "....................",
    "....................",
], {"k": "cat", "c": "catdk", "h": "pink", "d": "catdk", "t": "cathi"})

# ---------------------------------------------------------------- the coder (seen from behind)
# chair back
rect(140, 104, 26, 18, "chair")
rect(141, 105, 24, 1, "chairhi")
rect(152, 122, 3, 9, "metal")
rect(142, 131, 22, 2, "metal")
px(142, 133, "black"); px(163, 133, "black"); px(152, 133, "black")
# hoodie
rect(141, 92, 24, 13, "hood")
rect(143, 90, 20, 3, "hood")
rect(144, 90, 18, 1, "hoodhi")
rect(141, 92, 2, 12, "hooddk")
rect(163, 92, 2, 12, "hooddk")
rect(150, 92, 6, 3, "hooddk")  # hood folds
# arm reaching to the keyboard
for i in range(9):
    rect(140 - i, 95 + i // 2, 3, 3, "hood")
rect(130, 100, 4, 2, "skin")
# head, hair, headphones
rect(151, 89, 5, 3, "skin")
rect(151, 91, 5, 1, "skindk")
for y in range(70, 92):
    for x in range(141, 166):
        d = math.hypot(x - 153.0, y - 81.5)
        if d <= 8.8:
            px(x, y, "hair")
            if d > 6.8 and y < 79 and x < 152:
                px(x, y, "hairhi")
        elif d <= 10.3 and y <= 80:
            px(x, y, "phones" if d <= 9.6 else "phonesdk")
rect(141, 79, 4, 8, "phones")
rect(141, 86, 4, 1, "phonesdk")
rect(162, 79, 4, 8, "phones")
rect(162, 86, 4, 1, "phonesdk")

# ---------------------------------------------------------------- under the desk
rect(16, 114, 22, 26, "bezel")
rect(17, 115, 20, 1, "bezelhi")
rect(19, 118, 16, 1, "black")
rect(19, 121, 16, 1, "black")
rect(27, 132, 4, 4, "black")
rect(206, 114, 34, 24, "chair")
rect(206, 125, 34, 1, "black")
rect(220, 119, 6, 1, "metal")
rect(220, 130, 6, 1, "metal")
for x in range(38, 140):  # cable from the PC to the desk
    px(x, 113 + round(6 * math.sin((x - 38) / 102 * math.pi)), "greydk")
rect(178, 128, 12, 10, "greydk")  # bin
rect(179, 126, 10, 2, "white")

# ---------------------------------------------------------------- animated layers
use("stars")
for sx, sy in [(206, 18), (214, 26), (230, 14), (240, 30), (201, 36), (236, 42), (210, 40)]:
    if math.hypot(sx - cx, sy - cy) < r - 1:
        px(sx, sy, "white")
use("stars2")
for sx, sy in [(218, 20), (244, 24), (204, 28), (226, 30)]:
    if math.hypot(sx - cx, sy - cy) < r - 1:
        px(sx, sy, "c4")

use("neon")
# a neon "</>" sign (top left): glow, then tube, then highlight
pts = set()


def tube(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n)
        y = round(y0 + (y1 - y0) * i / n)
        pts.update({(x, y), (x + 1, y)})


tube(22, 14, 12, 24); tube(12, 24, 22, 34)      # <
tube(38, 13, 29, 35)                           # /
tube(45, 14, 55, 24); tube(55, 24, 45, 34)      # >
glow = set()
for (x, y) in pts:
    for ox in (-2, -1, 0, 1, 2):
        for oy in (-2, -1, 0, 1, 2):
            if abs(ox) + abs(oy) <= 2:
                glow.add((x + ox, y + oy))
for p in glow - pts:
    px(*p, "pinkglow")
for p in pts:
    px(*p, "pink")
for (x, y) in pts:
    if (x + 1, y) in pts and (x - 1, y) not in pts:
        px(x, y, "pinkhi")

use("leds")
for i, col in enumerate(["c1", "c2", "c3"]):
    rect(20 + i * 5, 126, 3, 2, col)

use("steam")
for sx, sy in [(178, 90), (180, 87), (179, 84), (182, 89), (183, 85), (181, 82)]:
    px(sx, sy, "#5a6488")

use("typing_preview")  # the preview shows the typing half done; the SVG animates it
rect(100, 97, 12, 1, "c3")
rect(113, 96, 1, 3, "white")

use("citylights")
px(233, 50, "citywin"); px(217, 58, "citywin")


# ---------------------------------------------------------------- output
def merged_rects(pixels):
    """Greedy rectangles: horizontal runs, then stack identical runs vertically."""
    runs = {}
    for y in range(H):
        x = 0
        while x < W:
            c = pixels.get((x, y))
            if c is None:
                x += 1
                continue
            x2 = x
            while x2 + 1 < W and pixels.get((x2 + 1, y)) == c:
                x2 += 1
            runs[(x, y)] = (x2 - x + 1, c)
            x = x2 + 1
    out = []
    used = set()
    for (x, y), (w, c) in sorted(runs.items(), key=lambda t: (t[0][1], t[0][0])):
        if (x, y) in used:
            continue
        h = 1
        while runs.get((x, y + h)) == (w, c) and (x, y + h) not in used:
            used.add((x, y + h))
            h += 1
        out.append((x, y, w, h, c))
    return out


def group(name, extra=""):
    by_colour = {}
    for x, y, w, h, c in merged_rects(layers[name]):
        by_colour.setdefault(c, []).append(f"M{x} {y}h{w}v{h}h-{w}z")
    paths = "".join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in by_colour.items())
    return f'<g id="{name}">{extra}{paths}</g>'


anim = {
    "stars": '<animate attributeName="opacity" values="1;.25;1" dur="3s" repeatCount="indefinite"/>',
    "stars2": '<animate attributeName="opacity" values=".2;1;.2" dur="4.5s" repeatCount="indefinite"/>',
    "neon": '<animate attributeName="opacity" values="1;1;.55;1;1;.8;1;1" keyTimes="0;.4;.42;.45;.7;.72;.75;1" dur="5s" repeatCount="indefinite"/>',
    "leds": '<animate attributeName="opacity" values="1;.35;1" dur="1.6s" repeatCount="indefinite"/>',
    "steam": '<animateTransform attributeName="transform" type="translate" values="0 2;0 -3" dur="2.4s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values="0;.9;0" dur="2.4s" repeatCount="indefinite"/>',
    "cursor": '<animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1s" repeatCount="indefinite"/>',
    "citylights": '<animate attributeName="opacity" values="1;1;0;0" calcMode="discrete" dur="6s" repeatCount="indefinite"/>',
}

# a code line that types itself out, next to the blinking cursor
steps = [0, 3, 6, 9, 12, 15, 18, 21, 24, 24, 24]
typing = ('<rect x="100" y="97" width="0" height="1" fill="#50fa7b">'
          f'<animate attributeName="width" values="{";".join(map(str, steps))}" calcMode="discrete" '
          'dur="4.4s" repeatCount="indefinite"/></rect>'
          '<rect x="100" y="96" width="1" height="3" fill="#e9ecf5">'
          f'<animate attributeName="x" values="{";".join(str(100 + v + 1) for v in steps)}" calcMode="discrete" '
          'dur="4.4s" repeatCount="indefinite"/>'
          '<animate attributeName="opacity" values="1;0" calcMode="discrete" dur=".8s" repeatCount="indefinite"/></rect>')
# warm light from the lamp
cone = '<path d="M27 82 L10 104 L58 104 L34 82 Z" fill="#ffd27a" opacity=".07"/>'

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="1280" height="720" '
    'shape-rendering="crispEdges" role="img" aria-labelledby="t">',
    '<title id="t">Pixel art of a coder at a desk in a room at night, with a neon sign, a round window and a sleeping cat</title>',
]
for name in order:
    if name == "typing_preview":
        continue
    svg.append(group(name, anim.get(name, "")))
    if name == "base":
        svg.append(cone)
svg.append(typing)
svg.append("</svg>")
parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
parser.add_argument("--preview", action="store_true", help="also write preview.png (needs Pillow)")
parser.add_argument("--out", type=Path, default=REPO, help="folder to write to (default: the repo root)")
args = parser.parse_args()

target = args.out / "pixel-banner.svg"
target.write_text("".join(svg), encoding="utf-8")
print(f"wrote {target} ({target.stat().st_size:,} bytes)")

if args.preview:
    from PIL import Image

    img = Image.new("RGB", (W, H))
    for name in order:
        for (x, y), c in layers[name].items():
            img.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)))
    img.resize((W * 5, H * 5), Image.NEAREST).save(args.out / "preview.png")
    print(f"wrote {args.out / 'preview.png'}")
