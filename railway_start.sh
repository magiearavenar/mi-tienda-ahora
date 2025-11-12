#!/bin/bash
echo "Starting Railway deployment..."

# Esperar a que la base de datos esté disponible
echo "Waiting for database..."
python -c "
import time
import psycopg2
import os
from urllib.parse import urlparse

db_url = os.environ.get('DATABASE_URL')
if db_url:
    parsed = urlparse(db_url)
    for i in range(30):
        try:
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:],
                connect_timeout=10
            )
            conn.close()
            print('Database is ready!')
            break
        except:
            print(f'Waiting for database... ({i+1}/30)')
            time.sleep(2)
    else:
        print('Database connection failed after 30 attempts')
        exit(1)
"

# Ejecutar migraciones
echo "Running migrations..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Iniciar servidor
echo "Starting server..."
python manage.py runserver 0.0.0.0:$PORT