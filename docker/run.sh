#!/bin/bash
set -e

echo "starting to run script"

# Ensure database directory exists and is writable
DB_PATH=${DB_PATH:-/app/data/analytics.db}
DB_DIR=$(dirname "$DB_PATH")
mkdir -p "$DB_DIR"
chmod 755 "$DB_DIR"

# Run migrations first
python manage.py migrate

# Start gunicorn
exec gunicorn conf.wsgi --log-file - --bind 0.0.0.0:8080

