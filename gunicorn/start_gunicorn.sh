#!/bin/bash
source /home/eliss/tg-helper/env/bin/activate
exec gunicorn -c "/home/eliss/tg-helper/gunicorn/gunicorn_conf.py" main:flask_app