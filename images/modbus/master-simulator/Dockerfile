FROM ubuntu:22.04

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"

RUN apt-get update
RUN apt-get install -y dnsutils

COPY modpoll-3.10.tgz /
COPY master.sh /


RUN tar -xzvpf modpoll-3.10.tgz


CMD [ "/master.sh"]