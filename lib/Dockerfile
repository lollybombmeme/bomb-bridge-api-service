FROM python:3.8.13-alpine3.16

RUN apk update && apk add --no-cache  tzdata git make  build-base


RUN apk upgrade -U \
    && apk add --no-cache -u ca-certificates libva-intel-driver libffi-dev  supervisor python3-dev build-base linux-headers pcre-dev curl busybox-extras \
    && rm -rf /tmp/* /var/cache/*

COPY requirements.txt requirements.txt
RUN pip --no-cache-dir install --upgrade pip setuptools wheel
RUN pip --no-cache-dir install -r requirements.txt
