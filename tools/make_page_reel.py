#!/usr/bin/env python3
"""make_page_reel.py SLIDES_DIR OUT.mp4 [VOICE.mp3|wav]

The magazine reel: a 10 s 9:16 flick through the seven carousel pages (slides/<name>/01..07.jpg).
  0.0- 1.5 s  the cover holds (the title is on it, readable with sound off on frame 0)
  then each page turns like a magazine page: the sheet rotates about the left spine, its free edge
  sweeping right-to-left with a little perspective and a shadow on the page beneath, 1.4 s a page;
  ends on the back cover (the save line) so it loops.
Each page becomes a full 9:16 sheet: a flat top or bottom edge colour (any palette) extends above and below
the 1080x1350 page; photo pages extend with a blurred, darkened copy of themselves. Frames are drawn with Pillow and
piped to ffmpeg (libx264, yuv420p, 30 fps). With VOICE (Samaira's line, TopView text-to-speech, Kelly) the line is the reel's own audio, loudness-normalised to -16 LUFS, and the pages follow the
voice: the line is written as seven phrases in page order, no comma inside a phrase, a <#x#> pause marker between
phrases (the brief varies x with the content; a marker gap is always longer than the voice's own breath at a full stop),
so the six longest gaps in the audio (ffmpeg silencedetect) are the page-turn cues and each page holds as long as its
phrase. The back cover holds until 0.4 s after the voice ends. Fewer than six gaps: fixed 1.4 s clock. Without a voice the reel is silent (the
trending track is added in the Instagram app either way).
Env: FFMPEG.
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter

src, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else None
FF = os.environ.get("FFMPEG", "ffmpeg")
W, H, FPS = 1080, 1920, 30
PW, PH = 1080, 1350
FOREST = (18, 62, 43)        # the ground behind a turning page
HOLD, TURN, SLIDE = 1.5, 0.5, 1.4            # cover hold, page-turn length, seconds per later page: 10.0 s total, nothing over 1.5 s
Y0 = (H - PH) // 2

def flat(page, y):
    """the page's colour at the top or bottom edge if a 200x24 patch there is one flat colour, else None"""
    patch = page.crop((PW // 2 - 100, y, PW // 2 + 100, y + 24))
    ex = patch.getextrema()
    if all(b - a < 10 for a, b in ex): return patch.getpixel((100, 12))
    return None

def sheet(page):
    """the page on its own 9:16 ground: above and below it, the page's own top/bottom colour when that is a
    paper colour (butter, lime, forest), otherwise a blurred, darkened copy of the page"""
    s = max(W / PW, H / PH); big = page.resize((round(PW * s), round(PH * s)), Image.BILINEAR)
    blur = big.crop(((big.width - W) // 2, (big.height - H) // 2, (big.width - W) // 2 + W, (big.height - H) // 2 + H))
    blur = Image.blend(blur.filter(ImageFilter.GaussianBlur(30)), Image.new("RGB", (W, H), FOREST), 0.45)
    bg = blur
    for edge, box in ((flat(page, 4), (0, 0, W, Y0)), (flat(page, PH - 28), (0, Y0 + PH, W, H))):
        if edge is not None:
            bg.paste(Image.new("RGB", (box[2] - box[0], box[3] - box[1]), edge), (box[0], box[1]))
    bg.paste(page, (0, Y0)); return bg

pages = [sheet(Image.open(os.path.join(src, f"{i:02d}.jpg")).convert("RGB").resize((PW, PH), Image.LANCZOS)) for i in range(1, 8)]

def ease(t): return t * t * (3 - 2 * t)          # ease-in-out: a page flip picks up, then settles

shadow = Image.new("RGBA", (W, 90), (0, 0, 0, 0))
for y in range(90): shadow.paste((0, 0, 0, int(140 * (1 - y / 90) ** 2)), (0, y, W, y + 1))

def persp(im, quad):
    """map the image's four corners (TL, TR, BR, BL) onto quad (same order) in the frame; returns RGBA frame layer"""
    import numpy as np
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad
    src = [(0, 0), (im.width, 0), (im.width, im.height), (0, im.height)]
    A, B = [], []
    for (X, Y), (u, v) in zip(quad, src):     # solve the 8 perspective coefficients: dest -> source
        A.append([X, Y, 1, 0, 0, 0, -u * X, -u * Y]); B.append(u)
        A.append([0, 0, 0, X, Y, 1, -v * X, -v * Y]); B.append(v)
    c = np.linalg.solve(np.array(A, float), np.array(B, float))
    rgba = im.convert("RGBA")
    return rgba.transform((W, H), Image.PERSPECTIVE, tuple(c), resample=Image.BILINEAR)

import re
def gaps(wav):
    """start times of the six longest silences (>= 0.12 s below -30 dB, not the lead-in or tail) in the voice, in time order, or None"""
    out = subprocess.run([FF, "-hide_banner", "-i", wav, "-af", "silencedetect=n=-30dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out); end = 60 * float(m.group(2)) + float(m.group(3))
    sil = [(float(s), float(e)) for s, e in zip(re.findall(r"silence_start: ([\d.]+)", out), re.findall(r"silence_end: ([\d.]+)", out))]
    sil = [(s, e) for s, e in sil if s > 0.3 and e < end - 0.3]
    if len(sil) < 6: return None
    return sorted(s for s, e in sorted(sil, key=lambda x: x[1] - x[0], reverse=True)[:6])

CUES = [HOLD + SLIDE * k for k in range(6)]     # when each page turn starts (page 2..7 arriving)
vlen = 0
if voice:
    vlen = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice]))
    g = gaps(voice)
    if g: CUES = [c + 0.05 for c in g]           # turn just as the phrase ends; the next phrase lands on the new page
    print("cues", [round(c, 2) for c in CUES])

def frame(i):
    t = i / FPS
    if t < CUES[0]: return pages[0].copy()
    k = max(j for j in range(6) if t >= CUES[j])   # which turn we are in (0 = page 2 arriving)
    tt = t - CUES[k]
    cur = k + 1
    prev = pages[cur - 1]; nxt = pages[cur]
    if tt >= TURN: return nxt.copy()
    p = ease(tt / TURN)
    # a magazine page turn: the current sheet rotates about the left spine, its free edge sweeping from
    # the right toward the spine; the next page lies underneath. As it folds it narrows (cos), its free
    # edge comes toward the viewer (a little taller), it darkens, and throws a soft shadow on the page below.
    import math
    th = p * math.pi / 2                          # 0 -> 90 degrees
    xe = W * math.cos(th)                         # free edge x
    lift = 0.10 * math.sin(th)                    # perspective: free edge taller by up to 10%
    quad = [(0, 0), (xe, -H * lift / 2), (xe, H * (1 + lift / 2)), (0, H)]
    bg = nxt.copy()
    # shadow on the page beneath, just right of the fold, fading with the turn
    sw = int(160 * (1 - p) + 20)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for x in range(sw):
        a = int(110 * (1 - x / sw) * math.sin(th))
        ImageDraw.Draw(sh).line([(round(xe) + x, 0), (round(xe) + x, H)], fill=(0, 0, 0, a))
    bg.paste(sh, (0, 0), sh)
    if xe > 2:
        sheet_im = Image.blend(prev, Image.new("RGB", (W, H), (0, 0, 0)), 0.35 * math.sin(th))
        layer = persp(sheet_im, quad)
        bg.paste(layer, (0, 0), layer)
    return bg

TOTAL = max(CUES[-1] + SLIDE + 0.1, vlen + 0.4)   # the back cover holds until the voice has finished
N = int(TOTAL * FPS)
audio = ["-i", voice, "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-c:a", "aac", "-b:a", "128k"] if voice else []
proc = subprocess.Popen([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", *audio, "-c:v", "libx264", "-preset", "medium",
                         "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(N): proc.stdin.write(frame(i).tobytes())
proc.stdin.close(); proc.wait()
assert proc.returncode == 0, "ffmpeg failed"
print(out, f"{N / FPS:.2f}s", N, "frames")
