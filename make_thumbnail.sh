#!/bin/bash

video_name="$1"
output_name="$2"

echo "Hello World!!"
echo $video_name
echo $output_name

echo $video_name $output_name >> output/test.txt

#./ffmpeg -i $video_name -filter:v fps=fps=1/2 extracted_frames/frame_%0d.bmp
##./ffmpeg -i $video_name -r 1/1 frame%03d.bmp
#
##time for i in {0..39};
###    do echo $i;
##    do ./ffmpeg -accurate_seek -ss `echo $i*60.0 | bc` -i vatanika.mp4 -frames:v 1 period_down_$i.bmp;
##done

