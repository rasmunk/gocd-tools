ARG BASE_IMAGE=debian:12
FROM $BASE_IMAGE AS builder

ARG PACKAGE_NAME=gocd_tools

USER root

RUN apt-get update && apt-get install --no-install-recommends -yq \
    ca-certificates \
    locales \
    python3-dev \
    python3-pip \
    python3-pycurl \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g configurable-http-proxy

ADD $PACKAGE_NAME /app/$PACKAGE_NAME
ADD setup.py /app/setup.py
ADD requirements.txt /app/requirements.txt
ADD requirements-dev.txt /app/requirements-dev.txt
ADD tests/requirements.txt /app/tests/requirements.txt

WORKDIR /app

RUN touch README.rst \
    && pip3 install . --break-system-packages

ENTRYPOINT ["gocd-tools"]