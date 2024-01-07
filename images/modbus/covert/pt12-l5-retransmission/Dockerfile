FROM covert-base:latest

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"
LABEL Covert="pt12"
LABEL Remarks="this covert channel sends one request every SEND_INTERVAL seconds. \
if the current byte pattern is matching, the request will be retransmitted. \
therefore this channel is really slow - use low send_interval values (<<1s)"
# Modbus layer 5 retransmission
# This covert channel basically retransmits modbus requests to the slave multiple times

ENV TARGET_HOST="modbus-slave"
ENV TARGET_PORT=502
ENV COVERT_MESSAGE="Y292ZXJ0LW1vZGJ1cy0xMg=="
ENV SEND_INTERVAL=1.0

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /app/
COPY app.py /app/


CMD [ "python", "/app/app.py"]