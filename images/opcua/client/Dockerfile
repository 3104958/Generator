FROM python:3.11

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"

ENV TARGET_HOST="opc-server"
ENV TARGET_PORT=4840

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py /

CMD [ "python", "/app.py"]
