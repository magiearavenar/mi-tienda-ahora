@echo off
echo Configurando proyecto Django...

echo Instalando dependencias...
pip install -r requirements.txt

echo Creando migraciones...
python manage.py makemigrations

echo Aplicando migraciones...
python manage.py migrate

echo Creando superusuario...
echo Ingresa los datos para el administrador:
python manage.py createsuperuser

echo.
echo ¡Proyecto configurado!
echo Para iniciar el servidor ejecuta: python manage.py runserver
echo Panel de admin: http://127.0.0.1:8000/admin/
pause