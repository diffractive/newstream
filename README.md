## Location of Gunicorn newstream app config
/etc/supervisor/conf.d/newstream.conf

## How to run Gunicorn:
sudo supervisorctl (start/stop/restart/status) newstream

## Minimum Requirements on Nginx Configuration:
client_max_body_size 12m;