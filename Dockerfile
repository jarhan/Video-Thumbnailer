# DOCKER-VERSION 0.3.4
FROM ubuntu:14.04

WORKDIR /

COPY ./make_thumbnail.sh /usr/local/bin/make_thumbnail.sh

RUN mkdir output

CMD /usr/local/bin/make_thumbnail.sh

ENTRYPOINT ["make_thumbnail.sh"]