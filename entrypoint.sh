#!/bin/bash

echo "Waiting for postgres..."
while ! python -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(('${DB_HOST}', int(${DB_PORT})))" 2>/dev/null; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL started"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate

echo "Initializing data..."
python manage.py initialize

exec "$@"
