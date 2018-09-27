# Milestone 1: The Basic Thumbnail Pipeline

The goal of this milestone is to make a Docker container that has all the relevant tools and a script/program that you write so that it can take a video file as input and generate an animated GIF file as output. The pipeline involves the following steps:

1.  Extract the frames that you wish to show in the output
2.  Resize the frames to the right size (pick one that is no smaller than 320x240.)
3.  Construct an animated GIF out of these frames.

Off-the-shelf tools can accomplish one or more of such tasks in a single command. You'll begin by researching how to make an animated GIF from a video file using command-line tools.

## Getting Started

Write a single script that, using a combination of tools, takes a video file as input and generates an animated GIF file as output. To have a controlled environment, your scripts and associated programs/packages will be housed in a (Docker) container.

### Prerequisites

- [Docker](https://www.docker.com/)

### Installing

```
git clone https://github.com/jarhan/Video-Thumbnailer.git
```

## Running the tests

Build Docker IMAGE named 'video_thumbnailer'

```
docker build -t video_thumbnailer .
```

Run Docker

```
docker run -v $(pwd)/resources:/resources video_thumbnailer make_thumbnail sample.mp4 output.gif
```

## Built With

This Docker use

- [ffmpeg](https://www.ffmpeg.org/) - Extract frames from video
- [imagemagick](http://www.imagemagick.org/script/index.php) - Create and resize .gif
