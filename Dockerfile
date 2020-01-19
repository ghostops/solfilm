FROM python:3.8-alpine

RUN pip3 install pipenv

# Imagemagick
RUN apk update
ENV MAGICK_HOME=/usr
RUN apk add --no-cache imagemagick && apk add --no-cache imagemagick-dev

# AWS
COPY .credentials/aws.txt /root/.aws/credentials

# FFMPEG
ENV FFMPEG_VERSION=4.2.2

RUN apk add --update build-base curl nasm tar bzip2 \
    zlib-dev openssl-dev yasm-dev lame-dev libogg-dev x264-dev libvpx-dev libvorbis-dev x265-dev freetype-dev libass-dev libwebp-dev rtmpdump-dev libtheora-dev opus-dev && \
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -s http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz | tar zxvf - -C . && \
    cd ffmpeg-${FFMPEG_VERSION} && \
    ./configure \
    --enable-version3 --enable-gpl --enable-nonfree --enable-small --enable-libmp3lame --enable-libx264 --enable-libx265 --enable-libvpx --enable-libtheora --enable-libvorbis --enable-libopus --enable-libass --enable-libwebp --enable-librtmp --enable-postproc --enable-avresample --enable-libfreetype --enable-openssl --disable-debug && \
    make && \
    make install && \
    make distclean && \
    rm -rf ${DIR} && \
    apk del build-base curl tar bzip2 x264 openssl nasm && rm -rf /var/cache/apk/*

WORKDIR /app

ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
ADD src src
ADD source source

RUN pipenv install --deploy --system
