#!/bin/bash
set -euo pipefail

cd /code/market-analyzer

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT:-5432}..."
while ! nc -z "${DB_HOST}" "${DB_PORT:-5432}"; do
  sleep 1
done
echo "PostgreSQL is ready."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn webapp.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --access-logfile - \
  --error-logfile -
