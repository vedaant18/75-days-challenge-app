#!/bin/bash
set -e

echo "Initializing database..."

# Create tables directly if no migrations exist yet
python -c "
from app import create_app
from app.extensions import db
app = create_app('production')
with app.app_context():
    db.create_all()
    print('Database tables ready!')
"

echo "Starting server..."
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 run:app
