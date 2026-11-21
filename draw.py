from PIL import Image, ImageDraw, ImageFont
import textwrap

W = H = 1024
BG = (247, 243, 234)      # ivory paper
INK = (18, 28, 46)        # near-black navy
NAVY = (16, 42, 78)
RED = (178, 34, 34)
GOLD = (176, 132, 30)
TEAL = (14, 110, 110)
GREEN = (34, 120, 60)
GREY = (90, 96, 110)

F_TITLE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 76)
F_KICKER = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
F_SUB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
F_HEAD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 29)
F_CAP = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
F_TAG = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 19)
F_FOOT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- header band ---
d.rectangle([0, 0, W, 176], fill=NAVY)
d.text((512, 26), "THE WORLD IN ONE IMAGE", font=F_KICKER, fill=(214, 182, 110), anchor="ma")
d.text((512, 58), "20 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255), anchor="ma")
d.text((512, 140), "Friday  •  The day's world news", font=F_SUB, fill=(200, 212, 228), anchor="ma")
# gold rule under header
d.rectangle([0, 176, W, 182], fill=(214, 182, 110))

def wrap(text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

panels = [
    ("NAYPYITAW", (16, 42, 78), "scales",
     "MYANMAR REJECTS GENOCIDE RULING",
     "A day after the world court found it guilty of genocide, Myanmar calls the 9\u20136 ruling \u2018unfair\u2019."),
    ("WASHINGTON", (178, 34, 34), "summit",
     "TRUMP DEFENDS SHENZHEN SUMMIT",
     "A day after the three-way meeting, Trump calls it \u2018electric\u2019 and defends sitting down with Xi and Putin."),
    ("KYIV", (120, 60, 20), "burst",
     "RUSSIA STRIKES KYIV OVERNIGHT",
     "Russia fires 110 missiles and 400 drones in its biggest attack of the year; nine killed and three Kyiv bridges hit."),
    ("RIYADH", (120, 30, 90), "tower",
     "RIYADH ON ALERT AFTER TOWER HIT",
     "A day after a Houthi missile damaged the PIF Tower, Saudi civil defence issues 15 air-threat alerts in Riyadh."),
    ("MARKETS", (14, 110, 110), "chart",
     "SELL-OFF DEEPENS INTO CORRECTION",
     "The S&P 500 falls 3.7% for a seventh straight loss and enters correction; Japan\u2019s Nikkei drops 5.1%."),
    ("ANTALYA", (34, 120, 60), "leaf",
     "COP31 TALKS SPILL INTO OVERTIME",
     "Negotiators miss Friday\u2019s deadline as the fossil-fuel fight stalls a deal; a new draft is due later today."),
]

def draw_icon(cx, cy, kind, color):
    r = 34
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    if kind == "scales":
        d.line([cx, cy-18, cx, cy+16], fill="white", width=4)
        d.line([cx-20, cy-12, cx+20, cy-12], fill="white", width=4)
        d.arc([cx-22, cy+2, cx-2, cy+20], 0, 180, fill="white", width=3)
        d.arc([cx+2, cy+2, cx+22, cy+20], 0, 180, fill="white", width=3)
        d.ellipse([cx-3, cy-22, cx+3, cy-16], fill="white")
    elif kind == "summit":
        for dx, col in ((-20, (70, 110, 200)), (0, (200, 60, 60)), (20, (230, 200, 60))):
            d.ellipse([cx+dx-11, cy-14, cx+dx+11, cy+8], fill=col, outline="white", width=2)
        d.arc([cx-22, cy+8, cx+22, cy+30], 180, 360, fill="white", width=3)
    elif kind == "burst":
        pts = []
        import math
        for i in range(16):
            ang = i * math.pi / 8
            rr = 24 if i % 2 == 0 else 10
            pts.append((cx + rr*math.cos(ang), cy + rr*math.sin(ang)))
        d.polygon(pts, fill=(255, 200, 60))
        d.ellipse([cx-6, cy-6, cx+6, cy+6], fill="white")
    elif kind == "tower":
        d.rectangle([cx-10, cy-20, cx+10, cy+20], fill="white")
        for yy in (-12, -2, 8):
            d.rectangle([cx-6, cy+yy, cx+6, cy+yy+4], fill=color)
        d.polygon([(cx, cy-30), (cx-7, cy-16), (cx+7, cy-16)], fill=(255, 170, 40))
    elif kind == "chart":
        d.line([(cx-22, cy+14), (cx-8, cy+2), (cx+4, cy+8), (cx+20, cy-14)], fill="white", width=4)
        d.polygon([(cx+20, cy-14), (cx+12, cy-14), (cx+20, cy-6)], fill="white")
    elif kind == "leaf":
        d.ellipse([cx-20, cy-20, cx+20, cy+20], outline="white", width=3)
        d.arc([cx-14, cy-14, cx+14, cy+14], 200, 340, fill="white", width=3)
        d.line([cx-14, cy+8, cx+14, cy-8], fill="white", width=3)

# --- grid: 2 cols x 3 rows ---
M, G = 24, 20
PW = (W - 2*M - G) // 2          # 480
PH = 250
y0 = 196
for i, (tag, color, icon, head, cap) in enumerate(panels):
    col, row = i % 2, i // 2
    x = M + col * (PW + G)
    y = y0 + row * (PH + 16)
    d.rounded_rectangle([x, y, x+PW, y+PH], radius=14, fill=(255, 255, 255),
                        outline=(210, 204, 190), width=2)
    # icon chip
    draw_icon(x + 52, y + 52, icon, color)
    d.text((x + 100, y + 28), tag, font=F_TAG, fill=color)
    # headline (max 2 lines)
    lines = wrap(head, F_HEAD, PW - 36)
    hy = y + 94
    for ln in lines[:2]:
        d.text((x + 18, hy), ln, font=F_HEAD, fill=INK)
        hy += 34
    # caption
    clines = wrap(cap, F_CAP, PW - 36)
    cy = hy + 4
    for ln in clines[:3]:
        d.text((x + 18, cy), ln, font=F_CAP, fill=(60, 66, 80))
        cy += 26

# --- footer ---
fy = y0 + 3 * PH + 2 * 14 + 6
d.rectangle([0, fy, W, H], fill=NAVY)
d.text((512, fy + 14), "All stories reported on 20 November 2026  •  Sources: ICJ, Dow Jones, OneTurn",
       font=F_FOOT, fill=(200, 212, 228), anchor="ma")

img.save("/home/hatch/workspace/makefun/news-image-20261120/entry.png", optimize=True)
print("saved")
