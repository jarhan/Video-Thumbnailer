# Build upon this image "alpine" is a lightweight distro
#FROM python:3.7-alpine
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y imagemagick
RUN apt-get install -y ffmpeg
RUN apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# Copy requirements.txt
COPY ./requirements.txt /app/requirements.txt

# Install all the requirements
RUN pip install -r /app/requirements.txt
RUN pip install requests

RUN mkdir resources
RUN mkdir resources/frames
RUN mkdir resources/gif
RUN mkdir resources/video

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app

# How to run it when we start up the box?
CMD ["./thumbnail_worker.py"]
