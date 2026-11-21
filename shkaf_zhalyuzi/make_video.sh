#!/bin/bash
# Сборка ролика: кадры 720×1280 -> 1080×1920, плавный переход в заставку с логотипом (2,5 с). Без звука.
set -e
cd "$(dirname "$0")"
ffmpeg -y -loglevel error -framerate 24 -i frames/%04d.png -loop 1 -t 2.5 -framerate 24 -i card.png -filter_complex \
 "[0:v]scale=1080:1920:flags=lanczos,format=yuv420p,setsar=1[a];[1:v]scale=1080:1920,format=yuv420p,setsar=1,fps=24[b];\
  [a][b]xfade=transition=fade:duration=0.6:offset=10.4[v]" -map "[v]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
 -movflags +faststart rustamyan-shkaf-oblet-reels.mp4
echo ok
