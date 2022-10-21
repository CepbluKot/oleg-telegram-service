#!/bin/sh

if [ -z ${STATUS_DOWNLOUD_BACKUP} ]; then
  echo "[SYSTEM BACKUP] -  NOT START DOWNLOUD BACKUP"
else
  if [ -z ${STATUS_DOWNLOUD_BACKUP} ]; then
    echo "[SYSTEM BACKUP] -  NOT START DOWNLOUD BACKUP ~ NOT FIND FILE"
  else
    echo "[SYSTEM BACKUP] -  START DOWNLOUD BACKUP"
    python3 ./backup_db/install_backup.py;
  fi
fi


if [ -z ${STATUS_CREATE_BACKUP} ]; then
  echo "[SYSTEM BACKUP] - NOT START INSTALLING BACKUP"
else
  if [ -z ${BACKUP_KEEP_SECONDS} ]; then
    echo "[SYSTEM BACKUP] - NOT START INSTALLING BACKUP- NOT FIND FILE"
  else
    echo "[SYSTEM BACKUP] - START INSTALLING BACKUP"
    while (true)
      do
        python3 ./backup_db/create_backup.py;
        sleep ${BACKUP_KEEP_SECONDS};
      done
  fi
fi
