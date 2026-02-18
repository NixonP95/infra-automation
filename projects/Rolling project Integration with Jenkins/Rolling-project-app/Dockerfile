FROM ubuntu:20.04 AS builder

ENV TZ=Asia/Jerusalem
ARG DEBIAN_FRONTEND=noninteractive

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
 && apt-get -y upgrade \
 && apt-get install -y --no-install-recommends \
      tzdata \
      iputils-ping \
      patchelf \
      git \
      openjdk-8-jdk \
      plantuml \
      doxygen \
      graphviz \
      xsltproc \
      python3-pip \
      curl \
      vim \
      cifs-utils \
      nfs-common \
 && apt-get -y autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir requests==2.22.0 Atlassian-python-API \
 && git config --global http.sslVerify false

RUN mkdir -p /home/ciuser/sdk /home/ciuser/.jfrog /home/ciuser/.ssh
