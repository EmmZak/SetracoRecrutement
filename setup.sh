#!/bin/bash

# Update package list and upgrade
sudo apt update && sudo apt upgrade -y

# Install necessary packages
sudo apt install -y python3 python3-pip git nginx

# Install Python dependencies
pip3 install django gunicorn


# nginx

server {
    server_name cvtheque.devexperimentation.fr www.cvtheque.devexperimentation.fr;

    access_log /var/log/nginx/cvtheque.log;

   location /media/ {
      root /home/ubuntu;
   }

    location /static/ {
        alias /home/ubuntu/SetracoRecrutement/staticfiles/;
    }

    location / {
        proxy_pass http://54.36.182.214:8000;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/cvtheque.devexperimentation.fr/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/cvtheque.devexperimentation.fr/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
    if ($host = cvtheque.devexperimentation.fr) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name cvtheque.devexperimentation.fr www.cvtheque.devexperimentation.fr;
    return 404; # managed by Certbot


}

# permissions
# Change ownership to nginx user (usually www-data)
sudo chown -R www-data:www-data /home/ubuntu/SetracoRecrutement/staticfiles
sudo chown -R www-data:www-data /home/ubuntu/media
sudo chown -R www-data:www-data /home/ubuntu/media/profile_files

# Ensure files are readable by nginx
sudo chmod -R 755 /home/ubuntu/SetracoRecrutement/staticfiles
sudo chmod -R 755 /home/ubuntu/media
sudo chmod -R 775 /home/ubuntu/media/profile_files

# Ensure that www-data has execute (x) permission on each parent directory
sudo chmod o+x /home/ubuntu
sudo chmod o+x /home/ubuntu/media
sudo chmod o+x /home/ubuntu/media/profile_files

sudo chown -R ubuntu:ubuntu /home/ubuntu/media # à tester au début 

OKOKOK 

drwxrwxr-x 2 ubuntu ubuntu   4096 Oct  7 17:27 profile_files/

(venv) ubuntu@vps-828d51f9:~/SetracoRecrutement$ ll /home/ubuntu/SetracoRecrutement/staticfiles/
total 28
drwxr-xr-x  4 www-data www-data  4096 Oct  6 20:24 ./
drwxrwxr-x 12 ubuntu   ubuntu    4096 Oct  7 10:30 ../
drwxr-xr-x  5 www-data www-data  4096 Oct  6 20:24 admin/
drwxr-xr-x  2 www-data www-data  4096 Oct  6 20:24 images/
-rwxr-xr-x  1 www-data www-data 10371 Oct  6 20:24 staticfiles.json*
