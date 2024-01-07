FROM covert-base:latest

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"
LABEL Covert="pt12"

ENV TARGET_HOST="opcplc"
ENV TARGET_PORT=50000
ENV COVERT_MESSAGE="hello world"

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /app/
COPY app.py /app/


CMD [ "python", "/app/app.py"]