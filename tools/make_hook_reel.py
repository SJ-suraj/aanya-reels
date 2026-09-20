#!/usr/bin/env python3
"""make_hook_reel.py TEXT.json OUT.mp4 IMG1 IMG2 IMG3

"Mistake reel": three 4:5 stills -> ~11.5 s 9:16 Reel with the hook burned on.
  0.0- 3.2 s  photo 1, HEADLINE (frame 0, big, readable with sound off) + place tag
  3.2- 6.2 s  photo 2, beat 1 (the mistake)
  6.2- 9.2 s  photo 3, beat 2 (what it costs you)
  9.2-11.5 s  photo 1, beat 3 (the fix) + CLOSE line; ends on photo 1 so it loops
Hard cuts, slow push-in on every shot, blurred fill behind the 4:5 frame.
TEXT.json: {"place": "PETRA · JORDAN", "headline": "...", "beats": ["...", "...", "..."], "close": "..."}
Env: FONT (path to a bold TTF; default DejaVu Sans Bold, then Arial Bold on macOS), FFMPEG.
"""
import json, os, subprocess, sys, tempfile, textwrap

text, out, imgs = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3:6]
FF = os.environ.get("FFMPEG", "ffmpeg")
FONT = os.environ.get("FONT") or next(p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if os.path.exists(p))
W, H, FPS = 1080, 1920, 30
SHOTS = [(0, 3.2), (1, 3.0), (2, 3.0), (0, 2.3)]          # (photo index, seconds)
beats = list(text["beats"])[:3]
assert len(beats) == 3, "three beats"
tmp = tempfile.mkdtemp()

def tf(name, s, width):
    p = os.path.join(tmp, name)
    open(p, "w").write("\n".join(textwrap.wrap(s, width)))
    return p

def draw(path, size, y, t0, t1, box_alpha=0.55):
    return (f"drawtext=fontfile='{FONT}':textfile='{path}':fontsize={size}:fontcolor=white:"
            f"line_spacing=10:x=(w-text_w)/2:y={y}:box=1:boxcolor=black@{box_alpha}:boxborderw=26:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2:enable='between(t,{t0},{t1})'")

inputs, layers, cuts, t = [], [], [], 0.0
for i, (img, secs) in enumerate(SHOTS):
    frames = int(secs * FPS)
    inputs += ["-loop", "1", "-t", f"{secs}", "-i", imgs[img]]
    layers.append(
        f"[{i}:v]split[b{i}][f{i}];"
        f"[b{i}]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=28,eq=brightness=-0.1[bg{i}];"
        f"[f{i}]scale=1080:1364,zoompan=z='min(zoom+0.0008,1.08)':d={frames}:s=1080x1364:fps={FPS}[fg{i}];"
        f"[bg{i}][fg{i}]overlay=(W-w)/2:(H-h)/2:shortest=1,setsar=1[v{i}]")
    cuts.append((t, t + secs)); t += secs
TOTAL = t

texts = [
    draw(tf("head.txt", text["headline"], 18), 84, 240, 0, cuts[0][1]),
    draw(tf("place.txt", text["place"], 30), 40, "h-170", 0, cuts[0][1], 0.45),
    draw(tf("b1.txt", beats[0], 26), 56, "h-text_h-330", cuts[1][0], cuts[1][1]),
    draw(tf("b2.txt", beats[1], 26), 56, "h-text_h-330", cuts[2][0], cuts[2][1]),
    draw(tf("b3.txt", beats[2], 26), 56, "h-text_h-400", cuts[3][0], TOTAL),
    draw(tf("close.txt", text["close"], 30), 44, "h-230", cuts[3][0] + 0.6, TOTAL, 0.45),
]
fc = ";".join(layers) + ";" + "".join(f"[v{i}]" for i in range(len(SHOTS))) + \
     f"concat=n={len(SHOTS)}:v=1:a=0,{','.join(texts)},format=yuv420p[v]"
cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex", fc, "-map", "[v]",
       "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print(out, f"{TOTAL:.1f}s", os.path.getsize(out))
