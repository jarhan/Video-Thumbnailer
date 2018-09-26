# DOCKER-VERSION 0.3.4
FROM ubuntu:16.04

WORKDIR /

RUN mkdir output

# FFMPEG
RUN apt-get update
RUN apt-get install -y ffmpeg
RUN apt-get install -y imagemagick

COPY ./make_thumbnail.sh /usr/local/bin/make_thumbnail

CMD ["make_thumbnail"]