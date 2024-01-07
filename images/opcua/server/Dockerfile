FROM python:3.11

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"

RUN apt-get update
RUN apt-get install -y netcat-openbsd

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py /
COPY custom_nodes.xml /

EXPOSE 4840/tcp

CMD [ "python", "/app.py"]
