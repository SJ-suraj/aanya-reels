#!/usr/bin/env python3
"""make_slides.py TEXT.json OUTDIR IMG1 IMG2 [IMG3]

Seven 4:5 carousel slides (1080x1350 JPEG) that read as one issue of a fashion magazine
(masthead, cover lines, issue line, barcode; inside pages as spreads). Two or three graded stills.
  01  COVER: photo 1 full bleed, masthead SAMAIRA across the top, the HOOK headline as the main
      cover line lower-left (sans + one serif-italic line), the three inside stories as small cover
      lines on the right, issue line and barcode at the foot
  02  CONTENTS: photo 2 full bleed, a contents column (03 the mistake / 04 what it costs / 06 the fix)
  03  SPREAD "THE MISTAKE": paper page, drop number, beat 1 as a pull quote, a small photo print
  04  THE RECEIPT "WHAT IT COSTS": the first number in beat 2 set huge, the sentence under it, receipt rules
  05  FULL PAGE: photo 3 clean with a one-line magazine credit
  06  SPREAD "THE FIX": as 03, beat 3
  07  BACK COVER: photo 1 top, paper below with "Save this for when you book <Place>", a second
      cover line, barcode
Type sizes follow the editorial guides (headline 64-96, body 28-50, labels 20-26 at 1080 wide); all
text stays inside the grid crop (34 px sides) and above the like/save band (bottom 200 px).
TEXT.json: {"place": "PETRA · JORDAN", "headline": "...", "beats": ["...", "...", "..."], "close": "..."}
Fonts: tools/fonts (OFL: Instrument Serif, Space Grotesk, DM Sans, IBM Plex Mono).
"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

text, outdir, imgs = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3:6]
assert len(imgs) in (2, 3), "two or three stills"
if len(imgs) == 2: imgs = imgs + [imgs[0]]
W, H = 1080, 1350
M = 80                                   # side margin: outside the 34 px grid crop with room to spare
PAPER, INK, ACCENT, MUTED = (243, 237, 224), (28, 26, 23), (200, 85, 61), (110, 104, 96)
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
def F(name, size): return ImageFont.truetype(os.path.join(FD, name), size)
SERIF, ITALIC = "InstrumentSerif-Regular.ttf", "InstrumentSerif-Italic.ttf"
SANS, BODY, MONO = "SpaceGrotesk-SemiBold.ttf", "DMSans-Medium.ttf", "IBMPlexMono-Regular.ttf"

beats = list(text["beats"])[:3]
assert len(beats) == 3, "three beats"
place_full = text["place"]                                 # "POSITANO · ITALY"
place = place_full.split("·")[0].strip()              # "POSITANO"
Place = place.title()
os.makedirs(outdir, exist_ok=True)

def photo(i, box=(W, H)):
    """cover-crop still i to box"""
    im = Image.open(imgs[i]).convert("RGB")
    s = max(box[0] / im.width, box[1] / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - box[0]) // 2, max(0, (im.height - box[1]) // 3)   # keep heads: crop from the top third
    return im.crop((x, y, x + box[0], y + box[1]))

def tw(d, s, f): return d.textbbox((0, 0), s, font=f)[2]
def th(f): a, b = f.getmetrics(); return a + b

def tracked(d, xy, s, f, fill, track=6, anchor="l"):
    """letter-spaced label; anchor l or r at xy"""
    w = sum(tw(d, c, f) for c in s) + track * (len(s) - 1)
    x, y = xy
    if anchor == "r": x -= w
    for c in s:
        d.text((x, y), c, font=f, fill=fill); x += tw(d, c, f) + track
    return w

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

def coverline(d, xy, s, size, fill, width, italic_last=True):
    """headline: sans lines, the last one serif italic (the cover-line pairing)"""
    x, y = xy
    sans, ital = F(SANS, size), F(ITALIC, round(size * 1.12))
    ls = lines(d, s, sans, width)
    for i, l in enumerate(ls):
        last = italic_last and i == len(ls) - 1 and len(ls) > 1
        f = ital if last else sans
        d.text((x, y), l, font=f, fill=fill); y += round(size * 1.04)
    return y

def barcode(d, x, y, w=150, h=44, fill=INK):
    import random
    r = random.Random(sum(map(ord, text["headline"])))
    xx = x
    while xx < x + w:
        bw = r.choice((2, 2, 3, 4, 5)); d.rectangle([xx, y, xx + bw - 1, y + h], fill=fill); xx += bw + r.choice((2, 3, 4))

def scrim(im, y0, y1, top_alpha, bot_alpha):
    """vertical gradient darkening between y0 and y1"""
    g = Image.new("L", (1, y1 - y0))
    for i in range(y1 - y0): g.putpixel((0, i), round(top_alpha + (bot_alpha - top_alpha) * i / max(1, y1 - y0 - 1)))
    im.paste(Image.new("RGB", (W, y1 - y0), (12, 10, 9)), (0, y0), g.resize((W, y1 - y0)))

def folio(d, n, dark=False):
    """issue line left, page number right, both above the UI band"""
    f, c = F(MONO, 20), (PAPER if dark else MUTED)
    issue = f"  ·  ISSUE {text['issue']}" if text.get("issue") else ""
    tracked(d, (M, H - 236), f"SAMAIRA  ·  {place_full}{issue}", f, c, 2)
    tracked(d, (W - M, H - 236), f"{n:02d} / 07", f, c, 2, "r")

def cover():
    im = photo(0); scrim(im, 0, 330, 120, 0); scrim(im, 700, H, 0, 175); d = ImageDraw.Draw(im)
    mast = F(SERIF, 196)
    d.text(((W - tw(d, "SAMAIRA", mast)) / 2, 118), "SAMAIRA", font=mast, fill=PAPER)
    tracked(d, (M, 98), "THE TRAVEL ISSUE", F(MONO, 22), PAPER, 5)
    tracked(d, (W - M, 98), place_full, F(MONO, 22), PAPER, 5, "r")
    # small cover lines (the inside stories) stacked over the main cover line, lower left
    tracked(d, (M, 640), "INSIDE", F(MONO, 22), PAPER, 6)
    y = 676
    for lab in ("THE MISTAKE", "WHAT IT COSTS", "THE FIX"):
        tracked(d, (M, y), lab, F(MONO, 22), PAPER, 5); y += 40
    d.line([M, y + 8, M + 120, y + 8], fill=PAPER, width=2)
    yy = coverline(d, (M, y + 32), text["headline"], 66, PAPER, 760)
    d.text((M, yy + 6), "swipe  →", font=F(MONO, 24), fill=PAPER)
    barcode(d, W - M - 150, yy + 6, fill=PAPER); folio(d, 1, True)
    return im

def contents():
    im = photo(1); scrim(im, 0, 260, 110, 0); scrim(im, 640, H, 0, 190); d = ImageDraw.Draw(im)
    tracked(d, (M, 98), "SAMAIRA", F(MONO, 22), PAPER, 6)
    tracked(d, (W - M, 98), "CONTENTS", F(MONO, 22), PAPER, 6, "r")
    y = 760
    for num, lab, blurb in (("03", "The mistake", "what everyone gets wrong"), ("04", "What it costs", "in real money"),
                            ("06", "The fix", "the thing to do instead")):
        d.text((M, y), num, font=F(SERIF, 54), fill=PAPER)
        d.text((M + 110, y + 4), lab, font=F(SANS, 40), fill=PAPER)
        d.text((M + 110, y + 54), blurb, font=F(ITALIC, 32), fill=PAPER)
        y += 104
    folio(d, 2, True)
    return im

def spread(n, num, label, body, src):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    tracked(d, (M, 98), "SAMAIRA", F(MONO, 22), MUTED, 6)
    tracked(d, (W - M, 98), place_full, F(MONO, 22), MUTED, 5, "r")
    # a small photo print, off-centre right, with a hairline border
    pw, ph = 300, 375
    pr = photo(src, (pw, ph)); im.paste(pr, (W - M - pw, 290))
    d.rectangle([W - M - pw - 1, 289, W - M, 290 + ph], outline=INK, width=1)
    d.text((M, 286), num, font=F(SERIF, 190), fill=ACCENT)
    tracked(d, (M + 4, 520), label, F(MONO, 24), INK, 6)
    d.line([M, 566, M + 120, 566], fill=INK, width=2)
    d.text((M, 690), "“", font=F(SERIF, 90), fill=ACCENT)
    yy = paragraph(d, (M, 760), body, F(SERIF, 54), INK, W - 2 * M - 40, 1.14)
    tracked(d, (M, min(yy + 24, H - 300)), f"PHOTOGRAPHED IN {place}", F(MONO, 20), MUTED, 4)
    folio(d, n)
    return im

def receipt(n, body):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    tracked(d, (M, 98), "SAMAIRA", F(MONO, 22), MUTED, 6)
    tracked(d, (W - M, 98), "02  /  WHAT IT COSTS", F(MONO, 22), MUTED, 5, "r")
    # the hero number: a price in the headline first (it is the mistake's cost), else the first in beat 2
    pat = r"(?:(€|\$|£|₹|¥)\s?)?(\d[\d,.]*)(?:\s?(euros?|dollars?|pounds?|rupees?|yen|dirhams?|baht|pesos?|francs?|[A-Z]{2,3}))?"
    m = next((x for x in re.finditer(pat, text["headline"]) if x.group(1) or x.group(3)), None) \
        or next((x for x in re.finditer(pat, body) if x.group(1) or x.group(3)), None) or re.search(pat, body)
    sym = {"euro": "€", "eur": "€", "€": "€", "dollar": "$", "usd": "$", "$": "$", "pound": "£", "gbp": "£", "£": "£",
           "rupee": "₹", "inr": "₹", "₹": "₹", "yen": "¥", "jpy": "¥", "¥": "¥"}
    d.line([M, 300, W - M, 300], fill=INK, width=2)
    d.text((M, 322), "R E C E I P T", font=F(MONO, 24), fill=INK)
    d.text((W - M - tw(d, place_full, F(MONO, 24)), 322), place_full, font=F(MONO, 24), fill=INK)
    for x in range(M, W - M, 14): d.line([x, 372, x + 7, 372], fill=INK, width=1)
    if m:
        unit = (m.group(3) or "").lower().rstrip("s")
        pre = m.group(1) or sym.get(unit, "")
        big = pre + m.group(2) + ("" if pre or not m.group(3) else " " + m.group(3))
        f = F(SERIF, 320 if len(big) <= 5 else 230)
        d.text((M - 8, 380), big, font=f, fill=INK)
        yy = d.textbbox((M - 8, 380), big, font=f)[3] + 16
    else:
        yy = 420
    for x in range(M, W - M, 14): d.line([x, yy + 10, x + 7, yy + 10], fill=INK, width=1)
    yy = paragraph(d, (M, yy + 44), body, F(BODY, 40), INK, W - 2 * M, 1.3)
    d.text((M, yy + 30), "TOTAL", font=F(MONO, 24), fill=ACCENT)
    d.text((W - M - tw(d, "the price of not knowing", F(ITALIC, 36)), yy + 22), "the price of not knowing", font=F(ITALIC, 36), fill=ACCENT)
    d.line([M, yy + 84, W - M, yy + 84], fill=INK, width=2)
    barcode(d, M, min(yy + 110, H - 300)); folio(d, n)
    return im

def fullpage():
    im = photo(2); scrim(im, 0, 240, 100, 0); scrim(im, 980, H, 0, 150); d = ImageDraw.Draw(im)
    tracked(d, (M, 98), "SAMAIRA", F(MONO, 22), PAPER, 6)
    tracked(d, (W - M, 98), place_full, F(MONO, 22), PAPER, 5, "r")
    d.text((M, 1010), f"{Place}, this summer. Shot on a friend's phone.", font=F(ITALIC, 34), fill=PAPER)
    folio(d, 5, True)
    return im

def back():
    im = Image.new("RGB", (W, H), PAPER)
    im.paste(photo(0, (W, 700)), (0, 0)); scrim(im, 0, 220, 110, 0); d = ImageDraw.Draw(im)
    tracked(d, (M, 98), "SAMAIRA", F(MONO, 22), PAPER, 6)
    tracked(d, (W - M, 98), "BACK COVER", F(MONO, 22), PAPER, 6, "r")
    coverline(d, (M, 770), f"Save this for when you book {Place}", 66, INK, W - 2 * M)
    d.text((M, 1000), text.get("close", "Send it to your person."), font=F(ITALIC, 36), fill=ACCENT)
    barcode(d, W - M - 150, 1000); folio(d, 7)
    return im

slides = [cover(), contents(), spread(3, "01", "THE MISTAKE", beats[0], 1), receipt(4, beats[1]),
          fullpage(), spread(6, "03", "THE FIX", beats[2], 0), back()]
for i, im in enumerate(slides, 1):
    p = os.path.join(outdir, f"{i:02d}.jpg"); im.save(p, quality=90, subsampling=0)
print(outdir, len(slides), "slides")
