#!/bin/bash

git pull

cd frontend

npm install

npm run build

sudo cp -r dist/* /usr/share/nginx/html
