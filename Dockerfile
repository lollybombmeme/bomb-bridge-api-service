FROM python:3.8-alpine

RUN apk update && apk add --no-cache  tzdata git make  build-base supervisor

RUN apk upgrade -U \
    && apk add --no-cache -u ca-certificates libffi-dev libva-intel-driver supervisor python3-dev build-base linux-headers pcre-dev curl busybox-extras \
    && rm -rf /tmp/* /var/cache/*
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev

COPY requirements.txt /
RUN pip --no-cache-dir install --upgrade pip setuptools wheel
RUN pip --no-cache-dir install -r requirements.txt
RUN pip --no-cache-dir install supervisor
RUN pip --no-cache-dir install "Flask[async]"


COPY conf/supervisor/ /etc/supervisor.d/
RUN mkdir -p /webapps/subprocess/
COPY . /webapps
WORKDIR /webapps
