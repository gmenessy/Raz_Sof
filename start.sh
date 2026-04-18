#!/bin/bash
set -e

# Wait for postgres to be ready
echo "Waiting for postgres..."
while ! python -c "import psycopg2, os; psycopg2.connect(os.environ['DATABASE_URL'])" 2>/dev/null; do
  sleep 1
done
echo "PostgreSQL started"

echo "Initializing database..."
python init_db.py

echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
