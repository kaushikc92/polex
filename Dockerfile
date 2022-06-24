FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y nginx vim python3 python3-pip
COPY frontend.conf /etc/nginx/conf.d/

WORKDIR /opt
COPY ./node-v16.15.1-linux-x64 ./node-v16.15.1-linux-x64

ENV NODEJS_HOME /opt/node-v16.15.1-linux-x64/bin
ENV PATH $NODEJS_HOME:$PATH

WORKDIR /ui
COPY ui/package.json .
COPY ui/package-lock.json .
COPY ui/src/ ./src/
COPY ui/public/ ./public/
RUN npm install
RUN npm run build

COPY entrypoint.sh /usr/local/bin/

WORKDIR /api
COPY api .
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["entrypoint.sh"]
