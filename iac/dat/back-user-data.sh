#!/bin/bash
# Actualizar el sistema
yum update -y

# Instalar dependencias
yum install -y git nginx python3 postgresql15 postgresql15-server

# Inicializar y arrancar PostgreSQL
/usr/bin/postgresql-setup --initdb
systemctl enable postgresql
systemctl start postgresql

# Clonar el repositorio del backend
cd /home/ec2-user
git clone https://github.com/Extantword/NASASPACEAPPS-EXO.git app
chown -R ec2-user:ec2-user app
cd app/backend

# Instalar dependencias de Python (ajusta si tu backend usa otro lenguaje)
pip3 install -r requirements.txt

# Configurar Nginx para redirigir el tráfico 80 -> 8080
cat > /etc/nginx/conf.d/backend.conf <<EOL
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL

# Eliminar configuración por defecto de Nginx
rm -f /etc/nginx/conf.d/default.conf

# Habilitar y reiniciar servicios
systemctl enable nginx
systemctl restart nginx
systemctl enable postgresql
systemctl restart postgresql

echo "Backend environment setup complete."
