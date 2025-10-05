#!/bin/bash

# Actualizar y dependencias
yum update -y

yum install -y curl git nginx

curl -fsSL https://rpm.nodesource.com/setup_22.x | bash -
yum install -y nodejs

# nginx config
systemctl enable nginx
systemctl start nginx

# app config
cd /home/ec2-user
git clone https://github.com/Extantword/NASASPACEAPPS-EXO.git app
chown -R ec2-user:ec2-user app
cd app/frontend

# Code Deploy
npm install
npm run build

rm -rf /usr/share/nginx/html/*
cp -r dist/* /usr/share/nginx/html/

chown -R nginx:nginx /usr/share/nginx/html

# Logging
{
  echo "✅ Setup completado con éxito"
  echo "Node.js version: $(node -v)"
  echo "Nginx version: $(nginx -v 2>&1)"
  echo "Git version: $(git --version)"
  echo "Repositorio: https://github.com/Extantword/NASASPACEAPPS-EXO.git"
} > /var/log/setup.log
