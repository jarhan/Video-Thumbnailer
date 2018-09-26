# Video-Thumbnailer
You are building a service that turns a user-supplied video file into a short animated-GIF thumbnail. As you might expect, it takes a nontrivial amount of time to extract the relevant frames and create an animated GIF out of them. To make the speed bearable to the users, we're setting a few parallel pipelines, which is the core technical lesson/challenge of this project.

This project consists of 3 milestones. They're aimed at splitting up work into smaller, manageable chunks:

* Milestone 1: Write a single script that, using a combination of tools, takes a video file as input and generates an animated GIF file as output. To have a controlled environment, your scripts and associated programs/packages will be housed in a (Docker) container.

* Milestone 2: Make the pipeline as a service. You'll wrap the pipeline from the previous milestone as a service that receives requests from a work queue and acts on such requests; it optionally announces to a status queue that the request is complete. To speed up the pipeline, we're aiming for you to run two parallel pipelines. You will have to set up the surrounding environment, including a work queue, plus a controller service that helps manage and monitor the requests.

* Milestone 3: Build a demo site. This will showcase the work we've done by letting the user upload video files and view the results as a webpage.


# Milestone 1: The Basic Thumbnail Pipeline
The goal of this milestone is to make a Docker container that has all the relevant tools and a script/program that you write so that it can take a video file as input and generate an animated GIF file as output. The pipeline involves the following steps:

1. Extract the frames that you wish to show in the output
2. Resize the frames to the right size (pick one that is no smaller than 320x240.)
3. Construct an animated GIF out of these frames.

Off-the-shelf tools can accomplish one or more of such tasks in a single command. You'll begin by researching how to make an animated GIF from a video file using command-line tools.

## Getting Started
Write a single script that, using a combination of tools, takes a video file as input and generates an animated GIF file as output. To have a controlled environment, your scripts and associated programs/packages will be housed in a (Docker) container.

### Prerequisites
* [Docker](https://www.docker.com/)

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
docker run -v /path/to/video/:/path/to/working_dir video_thumbnailer make_thumbnail sample.mp4 output.gif
```

## Built With
This Docker use 
* [ffmpeg](https://www.ffmpeg.org/) - Extract frames from video
* [imagemagick](http://www.imagemagick.org/script/index.php) - Create and resize .gif

## Version
p1-milestone1 is the version with **Milestone 1** done
```
git show p1-milestone
```

## Authors
* **Jarosporn Hansuekkaew** - [JarHan](https://github.com/jarhan)
