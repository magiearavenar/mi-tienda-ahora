#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

def test_server():
    try:
        # Probar importaciones
        from productos.models import Categoria, Tag, Producto
        print("✓ Modelos importados correctamente")
        
        # Probar admin
        from django.contrib import admin
        print("✓ Admin importado correctamente")
        
        # Probar que las categorías se pueden listar
        categorias = Categoria.objects.all()
        print(f"✓ Categorías en DB: {categorias.count()}")
        
        # Probar configuración
        from django.conf import settings
        print(f"✓ DEBUG: {settings.DEBUG}")
        
        print("\n=== SOLUCION ===")
        print("El error 500 puede ser por:")
        print("1. Reinicia el servidor completamente")
        print("2. Usa: python manage.py runserver --traceback")
        print("3. Esto te mostrará el error exacto")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_server()