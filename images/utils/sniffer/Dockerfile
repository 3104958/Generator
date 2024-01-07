FROM ubuntu:22.04

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"

ENV INTERFACE_NAME=lo
ENV SIM_NAME=unknown

RUN mkdir /pcaps
RUN apt-get update
RUN apt-get install -y tcpdump
COPY sniffer.sh /



CMD [ "/bin/bash", "/sniffer.sh"]
