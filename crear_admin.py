import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from django.contrib.auth.models import User

# Datos del nuevo admin
username = input("Nombre de usuario: ")
email = input("Email: ")
password = input("Contraseña: ")

# Crear usuario admin
if User.objects.filter(username=username).exists():
    print(f"El usuario '{username}' ya existe.")
else:
    User.objects.create_superuser(username, email, password)
    print(f"Usuario administrador '{username}' creado exitosamente!")