#!/bin/bash

video_name="$1"
output_name="$2"
min_w=320
min_h=240

# extract frames from video
ffmpeg -i resources/video/$video_name -ss 00:00:00 -vframes 20 -filter:v fps=fps=1/2 resources/frames/frame_%02d.bmp

# get image size
image_widht=$(convert resources/frames/frame_01.bmp -print "%wx%h" /dev/null | cut -d'x' -f1)
image_height=$(convert resources/frames/frame_01.bmp -print "%wx%h" /dev/null | cut -d'x' -f2)

# convert frame size for no smaller than 320x240
if [[ $image_height -lt $min_h ]]; then
image_widht=$(( $image_widht * $min_h / $image_height ))
image_height="$min_h"
fi

if [[ $image_widht -lt $min_w ]]; then
image_height=$(( $image_height * $min_w / $image_widht ))
image_widht="$min_w"
fi

gif_size=${image_widht}x${image_height}!

echo $gif_size

# generate .gif
convert -resize $gif_size -delay 30 -loop 0 resources/frames/frame_*.bmp resources/gif/$output_name

# delete created frames
rm -f resources/frames/frame_*.bmp
