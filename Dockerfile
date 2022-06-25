FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y nginx vim python3 python3-pip wget

COPY frontend.conf /etc/nginx/conf.d/

WORKDIR /opt

COPY ./node-v16.15.1-linux-x64 ./node-v16.15.1-linux-x64
ENV NODEJS_HOME /opt/node-v16.15.1-linux-x64/bin
ENV PATH $NODEJS_HOME:$PATH

COPY ./mongodb-linux-x86_64-ubuntu2004-5.0.9 ./mongodb-linux-x86_64-ubuntu2004-5.0.9
ENV MONGO_HOME /opt/mongodb-linux-x86_64-ubuntu2004-5.0.9/bin
ENV PATH $MONGO_HOME:$PATH

RUN wget https://repo.mongodb.org/apt/ubuntu/dists/focal/mongodb-org/5.0/multiverse/binary-amd64/mongodb-org-shell_5.0.9_amd64.deb
RUN dpkg -i mongodb-org-shell_5.0.9_amd64.deb

WORKDIR /ui
COPY ui/package.json .
COPY ui/package-lock.json .
COPY ui/src/ ./src/
COPY ui/public/ ./public/
RUN npm install

COPY entrypoint.sh /usr/local/bin/

WORKDIR /api
COPY api .
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["entrypoint.sh"]
