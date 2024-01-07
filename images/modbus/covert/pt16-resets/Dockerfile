FROM covert-base:latest


LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"
LABEL Covert="pt16"

# Modbus layer 5 retransmission
# This covert channel basically retransmits modbus requests to the slave multiple times

ENV TARGET_HOST="modbus-slave"
ENV TARGET_PORT=502
ENV COVERT_MESSAGE="Y292ZXJ0LW1vZGJ1cy0xNg=="

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /app/
COPY app.py /app/


CMD [ "python", "/app/app.py"]
