import os
from setting_backup import HeadBackupConfig

DB_HOSTNAME = os.getenv("DB_HOSTNAME", "localhost")
DB_NAME = os.getenv("DB_NAME", 'system_control')
DB_USER = os.getenv("DB_USER", 'postgres')
DB_PASSWORD = os.getenv("DB_PASSWORD", 'admin')

DB_FILENAME = "./backup_db.sql"


def delete_backup_on_ps():
    os.remove(DB_FILENAME)


def dump_database():
    print("Preparing database backup started")
    dump_db_operation_status = os.WEXITSTATUS(os.system(
        f"pg_dump -U {DB_USER} -W -h {DB_HOSTNAME} {DB_NAME} > {DB_FILENAME}"))
    if dump_db_operation_status != 0:
        exit(f"Dump database command exits with status "
             f"{dump_db_operation_status}.")
    print("DB dumped, archieved and encoded")


if __name__ == "__main__":
    dump_database()

    send_back = HeadBackupConfig()
    send_back.upload_file_yandex(DB_FILENAME)

    delete_backup_on_ps()
