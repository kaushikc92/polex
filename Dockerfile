FROM ubuntu:latest

WORKDIR /opt
COPY ./node-v16.15.1-linux-x64 ./node-v16.15.1-linux-x64

ENV NODEJS_HOME /opt/node-v16.15.1-linux-x64/bin
ENV PATH $NODEJS_HOME:$PATH

CMD tail -f /dev/null
