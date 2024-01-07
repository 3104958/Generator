FROM ubuntu:22.04

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"

RUN apt-get update
RUN apt-get install -y netcat-openbsd

COPY diagslave-3.4.tgz /
RUN tar -xzvpf diagslave-3.4.tgz

EXPOSE 502/tcp

CMD [ "/diagslave/x86_64-linux-gnu/diagslave", "-m", "tcp"]