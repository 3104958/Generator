FROM covert-base:latest


LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"
LABEL Covert="pt15"

ENV TARGET_HOST="modbus-slave"
ENV TARGET_PORT=502
ENV COVERT_MESSAGE="Y292ZXJ0LW1vZGJ1cy0xNQ=="

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /app/
COPY app.py /app/


CMD [ "python", "/app/app.py"]