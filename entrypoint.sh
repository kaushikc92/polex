#!/bin/bash

mkdir -p /storage/media/documents
mkdir -p /storage/media/tiles

mkdir -p /storage/public
(cd /ui && PUBLIC_URL="$CDRIVE_URL"app/"$COLUMBUS_USERNAME"/polex npm run build)
cp -r /ui/build/* /storage/public/

service nginx start &

python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8001
