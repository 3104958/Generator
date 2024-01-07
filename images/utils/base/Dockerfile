FROM python:3.11

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"

# common base image
# This image will be used as base image for other covert channels

RUN apt-get update
RUN pip install --upgrade pip
COPY requirements.txt requirements-base.txt
RUN pip install -r requirements-base.txt
RUN mkdir /app
COPY utilities.py /app/
COPY utilities_mqtt.py /app/
