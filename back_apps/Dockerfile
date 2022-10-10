FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3

RUN apt-get -y install python3-pip

COPY ./ tg_helper
RUN . /tg_helper/env/bin/activate && pip install -r /tg_helper/requirements.txt

ENV FLASK_APP=/tg_helper/main.py

CMD . /tg_helper/env/bin/activate
