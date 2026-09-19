#!/usr/bin/env bash
# make_reel.sh 01.png 02.png 03.png out.mp4  — three 4:5 stills -> 9:16 silent Reel, ~7.8 s
# each still held HOLD s with a slow push-in over a blurred copy of itself; XF s crossfades
set -euo pipefail
A=$1; B=$2; C=$3; OUT=$4
FF=${FFMPEG:-ffmpeg}
HOLD=3.0; XF=0.6; FPS=30
F=$(python3 -c "print(int($HOLD*$FPS))")
layer() { # $1 = input index
  echo "[$1:v]split[b$1][f$1];[b$1]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.08[bg$1];[f$1]scale=1080:1364,zoompan=z='min(zoom+0.0006,1.06)':d=$F:s=1080x1364:fps=$FPS[fg$1];[bg$1][fg$1]overlay=(W-w)/2:(H-h)/2:shortest=1,setsar=1,format=yuv420p[v$1]"
}
O1=$(python3 -c "print($HOLD-$XF)"); O2=$(python3 -c "print(2*($HOLD-$XF))")
"$FF" -y -hide_banner -loglevel error \
  -loop 1 -t $HOLD -i "$A" -loop 1 -t $HOLD -i "$B" -loop 1 -t $HOLD -i "$C" \
  -filter_complex "$(layer 0);$(layer 1);$(layer 2);[v0][v1]xfade=transition=smoothleft:duration=$XF:offset=$O1[x1];[x1][v2]xfade=transition=fade:duration=$XF:offset=$O2[v]" \
  -map "[v]" -r $FPS -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -movflags +faststart "$OUT"
