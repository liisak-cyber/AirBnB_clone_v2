#!/usr/bin/env bash
# This script sets up web servers for the deployment of web static

# Install Nginx if not already installed
if ! dpkg -s nginx > /dev/null 2>&1; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content
config="server {
    listen 80;
    listen [::]:80;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html index.htm;
    }
}"
echo "$config" | sudo tee /etc/nginx/sites-available/default > /dev/null

# Restart Nginx
sudo service nginx restart

