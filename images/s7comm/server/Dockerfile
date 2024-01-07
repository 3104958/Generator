FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TARGET_PORT=1102

RUN apt update \
    && apt install -y software-properties-common python3-pip netcat-openbsd \
    && add-apt-repository ppa:gijzelaar/snap7 \
    && apt update \
    && apt install -y libsnap7-dev libsnap7-1
EXPOSE 1102
ADD . /code
COPY starter.sh /
WORKDIR /code
RUN pip3 install -r /code/requirements.txt
RUN pip3 install .
CMD [ "/bin/bash", "/starter.sh"]