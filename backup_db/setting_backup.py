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
    backup_dir: str

    def __init__(self):
        self.yandex_disk = YaDisk(token= os.getenv("YANDEX_TOKEN", config['YANDEX_DISK']['TOKEN']))
        self.yandex_dir_back = os.getenv("YANDEX_DIR", config['YANDEX_DISK']['DIR_BACKUP'])
        self.backup_download_name = os.getenv("DB_FILENAME_DOWNLOAD", "./backup_db.dump")
        self.backup_install_name = os.getenv("DB_FILENAME_INSTALL", "backup_DAY_TIME_2022-10-18____17-23-46")

    def upload_file_yandex(self):
        if self.yandex_disk.check_token() and self.yandex_dir_back:
            today = datetime.today()

            try:
                dir_yandex = self.yandex_dir_back + f'/backup_DAY_TIME_' + f"{today.strftime('%Y-%m-%d____%H-%M-%S')}"
                print(dir_yandex)
                self.yandex_disk.upload(self.backup_download_name, dir_yandex)
            except PathNotFoundError:
                raise KeyError({"message": "not find folder in yandex disk"})
        else:
            raise ValueError({"message": "not correct data"})

    def download_file_yandex(self):
        if self.yandex_disk.check_token() and self.yandex_dir_back:
            try:
                dir_yandex = self.yandex_dir_back + '/' + self.backup_install_name
                print(dir_yandex)
                self.yandex_disk.download(dir_yandex, self.backup_download_name)
            except PathNotFoundError:
                raise KeyError({"message": "not find folder in yandex disk"})
        else:
            raise ValueError({"message": "not correct data"})
