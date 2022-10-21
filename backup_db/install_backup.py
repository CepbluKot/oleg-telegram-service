import os
from setting_backup import HeadBackupConfig

DB_HOSTNAME = os.getenv("DB_HOSTNAME", "localhost")
DB_NAME = os.getenv("DB_NAME", 'xui_db')
DB_USER = os.getenv("DB_USER", 'postgres')
DB_PASSWORD = os.getenv("DB_PASSWORD", 'admin')
DB_PORT = os.getenv("DB_PORT", 5432)

DB_FILENAME = "backup_db.dump"


def delete_backup_on_ps():
    os.remove(DB_FILENAME)


def restore_database():
    print("Preparing database backup started")
    restore_db_operation_status = os.WEXITSTATUS(os.system(
        f"psql -U {DB_USER} -h {DB_HOSTNAME} --port {DB_PORT} -d {DB_NAME} < {DB_FILENAME}"))
    if restore_db_operation_status != 0:
        exit(f"Dump database command exits with status "
             f"{restore_db_operation_status}.")
    print("DB dumped, archieved and encoded")


if __name__ == "__main__":
    down_back = HeadBackupConfig()
    down_back.download_file_yandex()

    restore_database()
    delete_backup_on_ps()