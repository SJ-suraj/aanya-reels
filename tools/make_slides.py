#!/usr/bin/env python3
"""make_slides.py TEXT.json OUTDIR IMG1 IMG2 [IMG3]

Seven 4:5 carousel slides (1080x1350 JPEG) from two or three graded stills and the HOOK text
(with two stills, slide 05 is photo 1 again without the headline):
  01  photo 1 + HEADLINE burned on (the cover: headline inside the centre square, so the profile grid
      and the top/bottom UI bands never hide it; under 40 characters reads without zooming; "swipe" cue)
  02  photo 2 + one-line promise (the second cover: Instagram re-serves the post opening on slide 2)
  03  text slide on a blurred, darkened photo 1: THE MISTAKE  + beat 1
  04  text slide: WHAT IT COSTS + beat 2
  05  photo 3, clean
  06  text slide: THE FIX + beat 3 (the slide people screenshot)
  07  blurred photo 1: one CTA only, "save this for when you book <place>", styled like the cover
Every slide carries "n / 7" (progress markers raise completion) and keeps text out of the top 270
and bottom 200 px (grid crop and the like/save overlay).
TEXT.json: {"place": "PETRA · JORDAN", "headline": "...", "beats": ["...", "...", "..."], "close": "..."}
Env: FONT (bold TTF; default DejaVu Sans Bold, then Arial Bold on macOS).
"""
import json, os, sys, textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageFont

text, outdir, imgs = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3:6]
assert len(imgs) in (2, 3), "two or three stills"
if len(imgs) == 2: imgs = imgs + [imgs[0]]
W, H = 1080, 1350
SAFE = 60 + 34           # 34 px each side is what the 3:4 grid crop removes; keep text inside
FONT = os.environ.get("FONT") or next(p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if os.path.exists(p))
beats = list(text["beats"])[:3]
assert len(beats) == 3, "three beats"
os.makedirs(outdir, exist_ok=True)

def font(size): return ImageFont.truetype(FONT, size)
def photo(i): return Image.open(imgs[i]).convert("RGB").resize((W, H), Image.LANCZOS)
def dark_blur(i, alpha=150):
    im = photo(i).filter(ImageFilter.GaussianBlur(22))
    im.paste(Image.new("RGB", (W, H), "black"), (0, 0), Image.new("L", (W, H), alpha))
    return im

def block(draw, lines, size, y, fill="white", spacing=12, box=None):
    """draw wrapped lines centred at y (top); returns bottom y"""
    f = font(size)
    heights = [draw.textbbox((0, 0), l, font=f)[3] for l in lines]
    total = sum(heights) + spacing * (len(lines) - 1)
    if box is not None:
        widths = [draw.textbbox((0, 0), l, font=f)[2] for l in lines]
        pad = 28
        draw.rounded_rectangle([(W - max(widths)) / 2 - pad, y - pad, (W + max(widths)) / 2 + pad, y + total + pad],
                               radius=18, fill=box)
    yy = y
    for l, h in zip(lines, heights):
        w = draw.textbbox((0, 0), l, font=f)[2]
        draw.text(((W - w) / 2 + 3, yy + 3), l, font=f, fill=(0, 0, 0, 160))
        draw.text(((W - w) / 2, yy), l, font=f, fill=fill)
        yy += h + spacing
    return yy

def wrap(s, width): return textwrap.wrap(s, width)

def chrome(d, n, place=True):
    """progress marker top-right and place tag bottom, both inside the safe bands"""
    f = font(30)
    d.text((W - SAFE - d.textbbox((0, 0), f"{n} / 7", font=f)[2], 290), f"{n} / 7", font=f, fill=(255, 255, 255, 230))
    if place:
        block(d, [text["place"]], 30, H - 260, fill=(230, 230, 230), box=(0, 0, 0, 110))

def cover():
    im = photo(0); d = ImageDraw.Draw(im)
    lines = wrap(text["headline"], 18)
    y = block(d, lines, 84, 360, box=(0, 0, 0, 150))
    block(d, ["swipe  \u2192"], 34, y + 60, fill=(255, 214, 102))
    chrome(d, 1)
    return im

def second():
    im = photo(1); d = ImageDraw.Draw(im)
    block(d, wrap("the mistake, what it costs, and the fix  \u2192", 26), 44, H - 420, box=(0, 0, 0, 140))
    chrome(d, 2)
    return im

def text_slide(n, label, body, src=0, body_size=66):
    im = dark_blur(src); d = ImageDraw.Draw(im)
    lines = wrap(body, 22)
    y = block(d, [label], 40, 400, fill=(255, 214, 102))
    block(d, lines, body_size, y + 50)
    chrome(d, n)
    return im

def fifth():
    im = photo(2); d = ImageDraw.Draw(im); chrome(d, 5); return im

def close():
    im = dark_blur(0, 170); d = ImageDraw.Draw(im)
    place = text["place"].split("\u00b7")[0].strip().title()
    block(d, wrap(f"Save this for when you book {place}", 18), 84, 460, box=(0, 0, 0, 150))
    chrome(d, 7)
    return im

slides = [cover(), second(), text_slide(3, "THE MISTAKE", beats[0]), text_slide(4, "WHAT IT COSTS", beats[1], 2),
          fifth(), text_slide(6, "THE FIX", beats[2], 1), close()]
for i, im in enumerate(slides, 1):
    p = os.path.join(outdir, f"{i:02d}.jpg"); im.save(p, quality=90, subsampling=0)
print(outdir, len(slides), "slides")
