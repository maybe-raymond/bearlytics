#!/bin/bash
set -e

echo "Starting bearlytics server..."

# Ensure database directory exists and is writable
DB_PATH=${DB_PATH:-/app/data/analytics.db}
DB_DIR=$(dirname "$DB_PATH")
mkdir -p "$DB_DIR"
chmod 755 "$DB_DIR"

# Verify Python and packages are available
echo "Checking Python installation..."
python --version
python -c "import django; print(f'Django {django.__version__} is available')" || {
    echo "ERROR: Django is not available. Check if packages were installed correctly."
    exit 1
}

# Run migrations first
echo "Running database migrations..."
python manage.py migrate --noinput

# Start gunicorn
echo "Starting Gunicorn server..."
exec gunicorn conf.wsgi --log-file - --bind 0.0.0.0:8080

