from betterconf import field, Config


class ConfConnect(Config):
    ip_adr = field('ip_adr', default='127.0.0.1')
    port = field('port', default='5000')
    type_connect = field('type_connect', default='http')


cfg_connect = ConfConnect()