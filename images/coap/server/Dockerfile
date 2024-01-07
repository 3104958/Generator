FROM ubuntu:22.04

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"
LABEL Source="libcoap2-bin"

RUN apt-get update
RUN apt-get install -y netcat-openbsd libcoap2-bin

EXPOSE 5683

CMD [ "/usr/bin/coap-server" ]