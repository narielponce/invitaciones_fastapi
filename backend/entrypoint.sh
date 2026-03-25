#!/bin/sh

# Si el comando es alembic, ejecutarlo directamente
if [ "$1" = "alembic" ]; then
  exec "$@"
fi

echo "⏳ Waiting for database..."
while ! nc -z db 3306; do
  sleep 1
done

echo "✅ Database is up!"

echo "🚀 Running migrations..."
alembic upgrade head

echo "🔥 Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
