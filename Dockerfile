# DOCKER-VERSION 0.3.4
FROM ubuntu:14.04

WORKDIR /

COPY ./make_thumbnail.sh /usr/local/bin/make_thumbnail

RUN mkdir output

#ENTRYPOINT ["make_thumbnail.sh"]

CMD ["make_thumbnail"]