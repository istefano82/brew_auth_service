#!/bin/sh
# sleep 1000
PROJECT="/usr/src/app"
RUN="python3 ${PROJECT}/manage.py"

run() {
  ${RUN} flush --no-input
  ${RUN} makemigrations
  ${RUN} migrate
  ${RUN} runserver ${HOST}:${PORT}
}

run