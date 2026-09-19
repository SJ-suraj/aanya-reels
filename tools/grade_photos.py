#!/usr/bin/env python3
"""grade_photos.py OUT_DIR IN1 [IN2 ...]

Film grade for the generated photos: Kodak Portra 400 look via postfx (pure CPU),
luminance-weighted grain, highlight roll-off, faint vignette, JPEG re-encode.
Writes OUT_DIR/01.jpg, 02.jpg, ... in input order. Env overrides:
  GRADE_THEME (default portra_400), GRADE_CONDITION (default neutral), GRADE_STRENGTH (0.85).
"""
import os, sys
import postfx

out_dir, inputs = sys.argv[1], sys.argv[2:]
theme = os.environ.get("GRADE_THEME", "portra_400")
condition = os.environ.get("GRADE_CONDITION", "neutral")
strength = float(os.environ.get("GRADE_STRENGTH", "0.85"))
os.makedirs(out_dir, exist_ok=True)
for i, src in enumerate(inputs, 1):
    dst = os.path.join(out_dir, f"{i:02d}.jpg")
    postfx.process_file(src, dst, theme=theme, condition=condition, strength=strength)
    print(dst, os.path.getsize(dst))
