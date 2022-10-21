import os
from yadisk import YaDisk
from yadisk.exceptions import PathNotFoundError
from configparser import ConfigParser
from datetime import datetime


config = ConfigParser()
config.read(os.path.abspath(os.path.dirname(__file__)) + '/connect_web.ini')

print((os.path.dirname(__file__)) + '/connect_web.ini')


class HeadBackupConfig:
    yandex_disk: YaDisk
    yandex_dir_back: str

    def __init__(self):
        self.yandex_disk = YaDisk(token= os.getenv("YANDEX_TOKEN", config['YANDEX_DISK']['TOKEN']))
        self.yandex_dir_back = os.getenv("YANDEX_DIR", config['YANDEX_DISK']['DIR_BACKUP'])

    def upload_file_yandex(self, dir_upload_file: str):
        if self.yandex_disk.check_token() and self.yandex_dir_back:
            today = datetime.today()

            try:
                self.yandex_disk.upload(dir_upload_file, self.yandex_dir_back + f'/backup')
            except PathNotFoundError:
                raise KeyError({"message": "not find folder in yandex disk"})
        else:
            raise ValueError({"message": "not correct data"})