#!/bin/sh
PROJECT="/usr/src/app"
RUN="python3 ${PROJECT}/manage.py"

db_check() {
  if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
}

run() {
  ${RUN} flush --no-input
  ${RUN} makemigrations
  ${RUN} migrate
  ${RUN} collectstatic --no-input --clear
  echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python3 manage.py shell
  ${RUN} runserver ${HOST}:${PORT}
}

db_check & run