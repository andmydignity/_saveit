#TODO:Make #4 it NGINX compatible.
sudo gunicorn -w 16 -b 0.0.0.0:443 --certfile=/etc/letsencrypt/live/DOMAINFOLDERHERE/fullchain.pem --keyfile=/etc/letsencrypt/live/DOMAINFOLDERHERE/privkey.pem main:site
