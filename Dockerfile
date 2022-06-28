FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y nginx vim python3 python3-pip wget

COPY nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /opt

RUN wget https://nodejs.org/dist/v16.15.1/node-v16.15.1-linux-x64.tar.xz
RUN tar -xf node-v16.15.1-linux-x64.tar.xz
ENV NODEJS_HOME /opt/node-v16.15.1-linux-x64/bin
ENV PATH $NODEJS_HOME:$PATH

WORKDIR /ui
COPY ui/package.json .
COPY ui/package-lock.json .
COPY ui/src/ ./src/
COPY ui/public/ ./public/
RUN npm install

WORKDIR /api
COPY api/requirements.txt .
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
COPY api .

COPY wkhtmltopdf /usr/local/bin/
COPY wkhtmltoimage /usr/local/bin/

COPY entrypoint.sh /usr/local/bin/

ENTRYPOINT ["entrypoint.sh"]
