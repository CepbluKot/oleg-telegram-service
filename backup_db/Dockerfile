FROM ubuntu:latest

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
    && apt-get install -y python3

RUN apt-get -y install python3-pip

RUN apt-get -y install postgresql

COPY ./ backup_db
RUN . /backup_db/env/bin/activate \
    && pip install -r /backup_db/req.txt

CMD . /backup_db/env/bin/activate