#!/bin/bash

bucket_name="$1"
object_name="$2"
min_w=320
min_h=240

echo $bucket_name
echo $object_name

mkdir resources/frames/${bucket_name}
mkdir resources/frames/${bucket_name}/${object_name}
mkdir resources/gif/${bucket_name}

# extract frames from video
ffmpeg -ss 00:00:00 -i resources/video/$bucket_name/$object_name -vframes 20 -filter:v fps=fps=1/2 resources/frames/${bucket_name}/${object_name}/frame_%02d.bmp

# get image size
image_widht=$(convert resources/frames/${bucket_name}/${object_name}/frame_01.bmp -print "%wx%h" /dev/null | cut -d'x' -f1)
image_height=$(convert resources/frames/${bucket_name}/${object_name}/frame_01.bmp -print "%wx%h" /dev/null | cut -d'x' -f2)

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
convert -resize $gif_size -delay 30 -loop 0 resources/frames/${bucket_name}/${object_name}/frame_*.bmp resources/gif/${bucket_name}/${object_name}.gif

# delete created frames
rm -f resources/frames/${bucket_name}/${object_name}/frame_*.bmp

echo "done"
