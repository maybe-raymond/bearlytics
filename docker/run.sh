#!/bin/bash
set -e

echo "starting to run script"

# Run migrations first
python manage.py migrate

# Start gunicorn
exec gunicorn conf.wsgi --log-file - --bind 0.0.0.0:8080

