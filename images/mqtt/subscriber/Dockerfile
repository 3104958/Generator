FROM covert-base:latest

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"

# Modbus layer 5 retransmission
# This covert channel basically retransmits modbus requests to the slave multiple times

ENV TARGET_HOST="emqx"
ENV TARGET_PORT=1883

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py /app/


CMD [ "python", "/app/app.py"]
