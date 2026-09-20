#!/usr/bin/env python3
"""grade_photos.py OUT_DIR IN1 [IN2 ...]

Film grade for the generated photos: Kodak Portra 400 look via postfx (pure CPU),
luminance-weighted grain, highlight roll-off, faint vignette, then a TEXTURE pass that
takes the plastic look off generated skin (the settings creators use for AI stills, 2026:
1.5-2.5 % monochrome luminance noise + faint chroma noise, a light unsharp mask, and two
JPEG rounds at camera-like qualities with 4:2:0 subsampling). Writes OUT_DIR/01.jpg, ... in
input order. Env overrides: GRADE_THEME (portra_400), GRADE_CONDITION (neutral),
GRADE_STRENGTH (0.85), TEXTURE_NOISE (percent of full scale, default 2.0; 0 disables).
"""
import io, os, sys
import numpy as np
import postfx
from PIL import Image, ImageFilter

def texture(path, noise_pct):
    """sensor-like grain + micro-contrast + camera JPEG rounds; in place"""
    im = Image.open(path).convert("RGB")
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=2))
    a = np.asarray(im).astype(np.float32)
    rng = np.random.default_rng(int.from_bytes(os.urandom(4), "little"))
    lum = rng.normal(0, 255 * noise_pct / 100, a.shape[:2])[..., None]      # monochrome grain
    chroma = rng.normal(0, 255 * noise_pct / 400, a.shape)                     # faint colour noise
    shade = 1.0 + (128 - a.mean(axis=2, keepdims=True)) / 512                 # a little more in the shadows
    a = np.clip(a + (lum + chroma) * shade, 0, 255).astype(np.uint8)
    im = Image.fromarray(a)
    for q in (90, 86):                                                          # two camera-like rounds
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, subsampling=2); buf.seek(0)
        im = Image.open(buf).convert("RGB")
    im.save(path, "JPEG", quality=92, subsampling=2)

out_dir, inputs = sys.argv[1], sys.argv[2:]
theme = os.environ.get("GRADE_THEME", "portra_400")
condition = os.environ.get("GRADE_CONDITION", "neutral")
strength = float(os.environ.get("GRADE_STRENGTH", "0.85"))
os.makedirs(out_dir, exist_ok=True)
for i, src in enumerate(inputs, 1):
    dst = os.path.join(out_dir, f"{i:02d}.jpg")
    postfx.process_file(src, dst, theme=theme, condition=condition, strength=strength)
    noise = float(os.environ.get("TEXTURE_NOISE", "2.0"))
    if noise > 0:
        texture(dst, noise)
    print(dst, os.path.getsize(dst))
