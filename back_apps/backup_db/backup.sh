#!/bin/sh

PATH=/etc:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

PGPASSWORD=admin
export PGPASSWORD
pathB=/tmp
dbUser=postgres
database=system_control

pg_dump -U $dbUser -W -h localhost $database > $pathB/backup_db.sql