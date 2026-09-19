#!/usr/bin/env bash
# make_montage.sh out.mp4 TOTAL_SECONDS img1 img2 ... imgN
# N stills -> one silent 9:16 Reel of TOTAL_SECONDS, hard cuts, every still shown for TOTAL/N seconds
# over a blurred, darkened copy of itself (same framing as make_reel.sh, no transitions).
set -euo pipefail
OUT=$1; TOTAL=$2; shift 2
FF=${FFMPEG:-ffmpeg}
N=$#
[ "$N" -ge 2 ] || { echo "need at least two images" >&2; exit 2; }
D=$(python3 -c "print(round($TOTAL/$N, 4))")
W=$(mktemp -d)
i=0
for img in "$@"; do
  i=$((i+1))
  "$FF" -y -hide_banner -loglevel error -i "$img" -filter_complex \
    "[0:v]split[b][f];[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.08[bg];[f]scale=1080:1364[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,format=yuv420p" \
    -frames:v 1 "$W/$(printf '%03d' $i).png"
  printf "file '%s'\nduration %s\n" "$W/$(printf '%03d' $i).png" "$D" >> "$W/list.txt"
done
# concat demuxer needs the last file repeated so its duration is honoured
printf "file '%s'\n" "$W/$(printf '%03d' $i).png" >> "$W/list.txt"
"$FF" -y -hide_banner -loglevel error -f concat -safe 0 -i "$W/list.txt" \
  -vf "fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 20 -movflags +faststart -t "$TOTAL" "$OUT"
rm -rf "$W"
