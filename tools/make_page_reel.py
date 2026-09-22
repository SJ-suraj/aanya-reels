#!/usr/bin/env python3
"""make_page_reel.py SLIDES_DIR OUT.mp4

The magazine reel: a ~11.5 s 9:16 flick through the seven carousel pages (slides/<name>/01..07.jpg).
  0.0- 2.6 s  the cover holds (the hook is on it, readable with sound off on frame 0)
  then each page slides up over the previous one with an ease-out, a soft page shadow, the outgoing
  page settling back a little, ~1.45 s a page; ends on the back cover (the save line) so it loops.
Pages sit on a forest ground at 1080x1350 inside the 1080x1920 frame. Frames are drawn with Pillow and
piped to ffmpeg (libx264, yuv420p, 30 fps, no audio: the trending track is added in the Instagram app).
Env: FFMPEG.
"""
import os, subprocess, sys
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
FF = os.environ.get("FFMPEG", "ffmpeg")
W, H, FPS = 1080, 1920, 30
PW, PH = 1080, 1350
FOREST = (18, 62, 43)
HOLD, TURN, SLIDE = 2.6, 0.55, 1.45          # cover hold, page-turn length, seconds per later page
pages = [Image.open(os.path.join(src, f"{i:02d}.jpg")).convert("RGB").resize((PW, PH), Image.LANCZOS) for i in range(1, 8)]
Y0 = (H - PH) // 2

def ease(t): return 1 - (1 - t) ** 3            # ease-out cubic

shadow = Image.new("RGBA", (W, 90), (0, 0, 0, 0))
for y in range(90): shadow.paste((0, 0, 0, int(140 * (1 - y / 90) ** 2)), (0, y, W, y + 1))

def frame(i):
    t = i / FPS
    bg = Image.new("RGB", (W, H), FOREST)
    if t < HOLD:
        bg.paste(pages[0], (0, Y0)); return bg
    k = int((t - HOLD) // SLIDE)                # which turn we are in (0 = page 2 arriving)
    tt = (t - HOLD) - k * SLIDE
    cur = min(k + 1, 6)
    prev = pages[cur - 1]; nxt = pages[cur]
    if tt >= TURN or cur == 6 and k > 5:
        bg.paste(nxt, (0, Y0)); return bg
    p = ease(tt / TURN)
    # the outgoing page settles back and darkens a touch; the incoming page slides up from below
    s = 1 - 0.06 * p
    pw, ph = round(PW * s), round(PH * s)
    small = prev.resize((pw, ph), Image.BILINEAR)
    dark = Image.new("RGB", (pw, ph), (0, 0, 0)); small = Image.blend(small, dark, 0.25 * p)
    bg.paste(small, ((W - pw) // 2, Y0 + (PH - ph) // 2))
    y = round(Y0 + (H - Y0) * (1 - p))
    if y - 90 < H: bg.paste(shadow, (0, y - 90), shadow)
    bg.paste(nxt, (0, y))
    return bg

TOTAL = HOLD + SLIDE * 6 + 0.2
N = int(TOTAL * FPS)
proc = subprocess.Popen([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                         "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(N): proc.stdin.write(frame(i).tobytes())
proc.stdin.close(); proc.wait()
assert proc.returncode == 0, "ffmpeg failed"
print(out, f"{N / FPS:.2f}s", N, "frames")
