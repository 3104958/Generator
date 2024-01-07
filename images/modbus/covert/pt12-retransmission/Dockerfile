FROM covert-base:latest

LABEL Maintainer="Katharina Lipsky <katharina.lipsky@studium.fernuni-hagen.de"
LABEL uses="N0dr4x TCPSession (https://gist.github.com/N0dr4x/) - modified by katharina lipsky"
LABEL Remarks="This covert channel was an early implementation which does not yet use convert_pattern() from the utilities"
LABEL Covert="pt12"

ENV TARGET_HOST="modbus-slave"
ENV TARGET_PORT=502
ENV COVERT_MESSAGE="Y292ZXJ0LW1vZGJ1cy0xMg=="

RUN apt-get update
RUN apt-get install -y iptables
RUN pip install --upgrade pip
RUN mkdir -p /app/
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY app.py /app/
COPY RetransmitClient.py /app/
COPY TcpSession.py /app/
COPY ClientInterface.py /app/


WORKDIR /app

CMD [ "python", "app.py"]
