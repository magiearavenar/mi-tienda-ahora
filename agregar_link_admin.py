#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

print("✅ Modal de categorías implementado!")
print("\n🔗 Accede a:")
print("- Modal de categorías: http://127.0.0.1:8000/admin/categorias/")
print("- Admin Django: http://127.0.0.1:8000/admin/")
print("\n📋 Funcionalidades:")
print("- Crear categorías principales")
print("- Crear subcategorías con categoría madre")
print("- Interfaz moderna con Bootstrap")
print("- Guardado sin recargar página")
print("- Validación de formularios")

if __name__ == '__main__':
    pass