#!/bin/bash

video_name="$1"
output_name="$2"
min_w=320
min_h=240

# extract frames from video
ffmpeg -i $video_name -filter:v fps=fps=1/2 output/frame_%0d.bmp

# get image size
image_widht=$(convert output/frame_1.bmp -print "%wx%h" /dev/null | cut -d'x' -f1)
image_height=$(convert output/frame_1.bmp -print "%wx%h" /dev/null | cut -d'x' -f2)

# convert frame size for no smaller than 320x240
if [[ $image_height < $min_h ]]; then
image_widht=$(( $image_widht * $min_h / $image_height ))
image_height="$min_h"
fi

if [[ $image_widht < $min_w ]]; then
image_height=$(( $image_height * $min_w / $image_widht ))
image_widht="$min_w"
fi

# generate .gif
convert -delay 60 -loop 0 output/frame_*.bmp output/animated.gif
