command = '/home/eliss/tg_helper/env/bin/gunicorn'
pythonpath = '/home/eliss/tg_helper/project/project'
bind = '127.0.0.1:8001'
workers = 5
user = 'eliss'
limit_request_fields = 32000
limit_request_field_size = 0
#raw_env = 'DJANGO_SETTINGS_MODULE=project.settings'