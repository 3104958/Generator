FROM python:3.11

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"

ENV TARGET_HOST="snap7-server"
ENV TARGET_PORT=1102
ENV SEND_INTERVAL=3.0

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py /

CMD [ "python", "/app.py"]
