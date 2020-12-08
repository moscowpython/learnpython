#!/usr/bin/env bash

set -e

DO_CONNECTION_CHECK=${DO_CONNECTION_CHECK:-true}

if [ "${DO_CONNECTION_CHECK}" = true ]; then
    for link in $(env | grep _LINK= | cut -d = -f 2 | sort | uniq)
    do
        /opt/app/wait-for-it.sh ${link} -t 0
    done
fi

LOG_LEVEL='DEBUG'

if [ "$1" == 'runworker' ]; then
    cd /opt/app
    exec gosu unprivileged celery -A landing_page worker -l info
fi

if [ "$1" == 'runserver' ]; then
    cd /opt/app
    exec gosu unprivileged gunicorn \
         -t 180 \
         --worker-tmp-dir /dev/shm \
         --access-logfile - \
         --error-logfile - \
         --log-level info \
         --workers 8 \
         --bind 0.0.0.0:8000 \
    landing_page.wsgi:application
fi

exec "$@"
