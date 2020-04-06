#!/bin/sh
# sleep 1000
PROJECT="/usr/src/app"
RUN="python3 ${PROJECT}/manage.py"

run() {
  ${RUN} flush --no-input
  ${RUN} makemigrations
  ${RUN} migrate
  echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python3 manage.py shell
  ${RUN} runserver ${HOST}:${PORT}
}

run