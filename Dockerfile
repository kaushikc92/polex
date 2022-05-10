FROM python:3

RUN apt-get update && apt-get install -y vim

COPY wkhtmltopdf /usr/local/bin/
COPY wkhtmltoimage /usr/local/bin/

WORKDIR /src
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY ./src/ .

EXPOSE 8000

CMD tail -f /dev/null
