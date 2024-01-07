FROM ubuntu:22.04

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"
LABEL Source="libcoap2-bin"

ENV SEND_INTERVAL=1.0

RUN apt-get update
RUN apt-get install -y libcoap2-bin

COPY app.sh /
RUN chmod +x /app.sh

CMD [ "/app.sh"]