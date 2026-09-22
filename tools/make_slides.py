#!/usr/bin/env python3
"""make_slides.py TEXT.json OUTDIR IMG1 IMG2 [IMG3]

Seven 4:5 carousel slides (1080x1350 JPEG) set like an issue of a fashion magazine in the Off Centre
palette (forest #123E2B, butter #F5E7A8, lime #D9EF78, cream #FFF9E7). Her photo is on every page.
  01  COVER: photo 1 full bleed, the SAMAIRA masthead rotated up a forest band on the left, the HOOK
      headline as the cover line lower-left, a lime sticker naming the three inside stories
  02  INSIDE: butter page, photo 2 as a tilted print, the contents list (pages 3, 4, 6)
  03  THE MISTAKE: butter page, photo 1 cut into three offset strips across the top, beat 1 as a serif pull quote
  04  WHAT IT COSTS: lime page, the price from the headline set huge, beat 2 under it, a small print of photo 2
  05  FULL PAGE: photo 3 full bleed, a forest band at the foot with one credit line
  06  THE FIX: as 03 with photo 2 and beat 3
  07  BACK COVER: photo 1 top, lime block below with "Save this for when you book <Place>" and the send line
Type: Instrument Serif (masthead, quotes, the number), Space Grotesk (cover lines), DM Sans (small text,
sentence case). Sizes follow the editorial guides (cover line 64-72, quotes 50-54, small 24-28 at 1080 wide);
text stays inside the 3:4 grid crop (34 px sides) and above the like/save band (bottom 200 px).
TEXT.json: {"place": "PETRA · JORDAN", "headline": "...", "beats": ["...", "...", "..."], "close": "..."}
Fonts: tools/fonts (OFL: Instrument Serif, Space Grotesk, DM Sans).
"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

text, outdir, imgs = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3:6]
assert len(imgs) in (2, 3), "two or three stills"
if len(imgs) == 2: imgs = imgs + [imgs[0]]
W, H = 1080, 1350
M = 80                                   # side margin: outside the 34 px grid crop with room to spare
FOREST, BUTTER, LIME, CREAM, OLIVE = (18, 62, 43), (245, 231, 168), (217, 239, 120), (255, 249, 231), (83, 98, 75)
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
def F(name, size): return ImageFont.truetype(os.path.join(FD, name), size)
SERIF, ITALIC = "InstrumentSerif-Regular.ttf", "InstrumentSerif-Italic.ttf"
SANS, BODY = "SpaceGrotesk-SemiBold.ttf", "DMSans-Medium.ttf"

beats = list(text["beats"])[:3]
assert len(beats) == 3, "three beats"
parts = [p.strip() for p in text["place"].split("·")]          # "POSITANO · ITALY"
Place = parts[0].title()
Country = parts[1].title() if len(parts) > 1 else ""
place_line = f"{Place}, {Country}" if Country else Place
os.makedirs(outdir, exist_ok=True)

def photo(i, box=(W, H), top=1 / 3):
    """cover-crop still i to box; crop from the top third so heads stay in"""
    im = Image.open(imgs[i]).convert("RGB")
    s = max(box[0] / im.width, box[1] / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - box[0]) // 2, max(0, round((im.height - box[1]) * top))
    return im.crop((x, y, x + box[0], y + box[1]))

def tw(d, s, f): return d.textbbox((0, 0), s, font=f)[2]

def lines(d, s, f, width):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= width: cur = t
        else: out.append(cur); cur = w
    return out + [cur] if cur else out

def paragraph(d, xy, s, f, fill, width, lead=1.18):
    x, y = xy
    for l in lines(d, s, f, width):
        d.text((x, y), l, font=f, fill=fill); y += round(f.size * lead)
    return y

def coverline(d, xy, s, size, fill, width):
    """the Off Centre pairing: sans lines, the last line serif italic"""
    x, y = xy
    sans, ital = F(SANS, size), F(ITALIC, round(size * 1.14))
    ls = lines(d, s, sans, width)
    for i, l in enumerate(ls):
        f = ital if (i == len(ls) - 1 and len(ls) > 1) else sans
        d.text((x, y), l, font=f, fill=fill); y += round(size * 1.04)
    return y

def scrim(im, y0, y1, a0, a1, colour=(8, 30, 20)):
    g = Image.new("L", (1, y1 - y0))
    for i in range(y1 - y0): g.putpixel((0, i), round(a0 + (a1 - a0) * i / max(1, y1 - y0 - 1)))
    im.paste(Image.new("RGB", (W, y1 - y0), colour), (0, y0), g.resize((W, y1 - y0)))

def folio(d, n, fill):
    """issue line left, page count right, above the UI band"""
    f = F(BODY, 22)
    d.text((M, H - 236), f"Samaira, {place_line}", font=f, fill=fill)
    s = f"{n} of 7"; d.text((W - M - tw(d, s, f), H - 236), s, font=f, fill=fill)

def strips(im, src, y, h, offsets, gap=6):
    """the sliced-photo move: the same photo in horizontal strips, each shifted sideways"""
    src_im = photo(src, (W - 2 * M, h), top=0.15)
    n = len(offsets); sh = (h - gap * (n - 1)) // n
    for k, off in enumerate(offsets):
        strip = src_im.crop((0, k * (sh + gap), W - 2 * M, k * (sh + gap) + sh))
        x = M + off
        if x < 0: strip = strip.crop((-x, 0, strip.width, sh)); x = 0
        if x + strip.width > W: strip = strip.crop((0, 0, W - x, sh))
        im.paste(strip, (x, y + k * (sh + gap)))

def tilted_print(im, src, box, xy, angle, border=CREAM):
    pr = photo(src, box, top=0.2)
    fr = Image.new("RGB", (box[0] + 28, box[1] + 28), border); fr.paste(pr, (14, 14))
    rot = fr.rotate(angle, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
    mask = Image.new("L", fr.size, 255).rotate(angle, expand=True, resample=Image.BICUBIC)
    im.paste(rot, xy, mask)

def sticker(d, cx, cy, r, lines_, size):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LIME)
    f = F(BODY, size); lh = round(size * 1.15); y = cy - lh * len(lines_) / 2 + 2
    for l in lines_:
        d.text((cx - tw(d, l, f) / 2, y), l, font=f, fill=FOREST); y += lh

def cover():
    im = photo(0); scrim(im, 0, 260, 120, 0); scrim(im, 720, H, 0, 190); d = ImageDraw.Draw(im)
    band = 150
    d.rectangle([0, 0, band, H], fill=FOREST)
    mast = F(SERIF, 150)
    txt = Image.new("RGBA", (tw(d, "SAMAIRA", mast) + 40, 170), (0, 0, 0, 0))
    ImageDraw.Draw(txt).text((20, -14), "SAMAIRA", font=mast, fill=BUTTER)
    txt = txt.rotate(90, expand=True)
    im.paste(txt, (band // 2 - txt.width // 2, 300), txt)
    d.text((band + 30, 98), "The travel issue", font=F(BODY, 26), fill=CREAM)
    s = place_line; d.text((W - M - tw(d, s, F(BODY, 26)), 98), s, font=F(BODY, 26), fill=CREAM)
    sticker(d, W - M - 130, 520, 118, ["the mistake,", "the cost,", "the fix"], 26)
    x = band + 60
    yy = coverline(d, (x, 780), text["headline"], 68, CREAM, W - x - M)
    d.text((x, yy + 34), "swipe", font=F(BODY, 24), fill=LIME)
    folio(d, 1, CREAM)
    return im

def inside():
    im = Image.new("RGB", (W, H), BUTTER); d = ImageDraw.Draw(im)
    d.text((M, 98), "Samaira", font=F(BODY, 26), fill=FOREST)
    tilted_print(im, 1, (470, 590), (520, 250), -6)
    d.text((M, 300), "Inside", font=F(SANS, 96), fill=FOREST)
    d.text((M, 410), "this issue.", font=F(ITALIC, 108), fill=FOREST)
    y = 620
    for num, lab, blurb in (("3", "The mistake", "what everyone gets wrong"), ("4", "What it costs", "in real money"),
                            ("6", "The fix", "what to do instead")):
        d.text((M, y), num, font=F(SERIF, 64), fill=FOREST)
        d.text((M + 70, y + 8), lab, font=F(SANS, 40), fill=FOREST)
        d.text((M + 70, y + 60), blurb, font=F(ITALIC, 34), fill=OLIVE)
        y += 124
    folio(d, 2, OLIVE)
    return im

def spread(n, label, body, src, offsets):
    im = Image.new("RGB", (W, H), BUTTER); d = ImageDraw.Draw(im)
    strips(im, src, 250, 480, offsets)
    d.text((M, 98), "Samaira", font=F(BODY, 26), fill=FOREST)
    s = label; d.text((W - M - tw(d, s, F(BODY, 26)), 98), s, font=F(BODY, 26), fill=FOREST)
    d.text((M - 6, 750), "“", font=F(SERIF, 120), fill=FOREST)
    paragraph(d, (M, 830), body, F(SERIF, 54), FOREST, W - 2 * M, 1.12)
    folio(d, n, OLIVE)
    return im

def cost(n, body):
    im = Image.new("RGB", (W, H), LIME); d = ImageDraw.Draw(im)
    d.text((M, 98), "Samaira", font=F(BODY, 26), fill=FOREST)
    s = "What it costs"; d.text((W - M - tw(d, s, F(BODY, 26)), 98), s, font=F(BODY, 26), fill=FOREST)
    pat = r"(?:(€|\$|£|₹|¥)\s?)?(\d[\d,.]*)(?:\s?(euros?|dollars?|pounds?|rupees?|yen|dirhams?|baht|pesos?|francs?|[A-Z]{2,3}))?"
    sym = {"euro": "€", "dollar": "$", "pound": "£", "rupee": "₹", "yen": "¥"}
    m = next((x for x in re.finditer(pat, text["headline"]) if x.group(1) or x.group(3)), None) \
        or next((x for x in re.finditer(pat, body) if x.group(1) or x.group(3)), None) or re.search(pat, body)
    yy = 300
    if m:
        unit = (m.group(3) or "").lower().rstrip("s"); pre = m.group(1) or sym.get(unit, "")
        big = pre + m.group(2) + ("" if pre or not m.group(3) else " " + m.group(3))
        f = F(SANS, 300 if len(big) <= 4 else 210)
        d.text((M - 10, 250), big, font=f, fill=FOREST)
        yy = d.textbbox((M - 10, 250), big, font=f)[3] + 40
    yy = paragraph(d, (M, yy), body, F(SERIF, 54), FOREST, 620, 1.12)
    tilted_print(im, 1, (300, 380), (W - M - 330, H - 700), 5, border=FOREST)
    d.text((M, min(yy + 30, H - 300)), "Not in the guidebook.", font=F(ITALIC, 34), fill=OLIVE)
    folio(d, n, FOREST)
    return im

def fullpage():
    im = photo(2); scrim(im, 0, 240, 110, 0); d = ImageDraw.Draw(im)
    d.rectangle([0, H - 340, W, H], fill=FOREST)
    d.text((M, 98), "Samaira", font=F(BODY, 26), fill=CREAM)
    d.text((M, H - 340 + 30), f"{Place}, this summer.", font=F(ITALIC, 44), fill=BUTTER)
    folio(d, 5, CREAM)
    return im

def back():
    im = Image.new("RGB", (W, H), LIME)
    im.paste(photo(0, (W, 720), top=0.2), (0, 0)); d = ImageDraw.Draw(im)
    d.text((M, 98), "Samaira", font=F(BODY, 26), fill=CREAM)
    yy = coverline(d, (M, 790), f"Save this for when you book {Place}", 66, FOREST, W - 2 * M)
    d.text((M, yy + 24), text.get("close", f"Send it to whoever booked {Place}"), font=F(BODY, 28), fill=FOREST)
    folio(d, 7, FOREST)
    return im

slides = [cover(), inside(), spread(3, "The mistake", beats[0], 0, (-40, 24, -8)), cost(4, beats[1]),
          fullpage(), spread(6, "The fix", beats[2], 1, (24, -40, 8)), back()]
for i, im in enumerate(slides, 1):
    p = os.path.join(outdir, f"{i:02d}.jpg"); im.save(p, quality=90, subsampling=0)
print(outdir, len(slides), "slides")
