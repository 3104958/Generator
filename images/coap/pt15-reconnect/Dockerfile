FROM covert-base:latest

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"
LABEL Source="another implementation heavily inspired by https://github.com/NIoSaT/CoAP-Covert-Channels"
LABEL Covert="pt15"

ENV TARGET_HOST="coap-server"
ENV TARGET_PORT=5683
ENV COVERT_VICTIMS=0
ENV COVERT_MESSAGE="Y292ZXJ0LW1xdHQtMTU="

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /app/
COPY app.py /app/



CMD [ "python", "/app/app.py"]
