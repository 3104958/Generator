FROM covert-base:latest

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"
LABEL Covert="pt15"

# mqtt reconnect pattern
# This covert channel basically reconnects other clients

ENV TARGET_HOST="emqx"
ENV TARGET_PORT=1883
ENV COVERT_VICTIMS=2
ENV COVERT_MESSAGE="Y292ZXJ0LW1xdHQtMTU="

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /app/
COPY app.py /app/


CMD [ "python", "/app/app.py"]
