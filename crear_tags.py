#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import Tag, Categoria

def crear_tags():
    # Tags de ejemplo para papelería
    tags_data = [
        {'nombre': 'papelería', 'color': '#3498db'},
        {'nombre': 'agendas', 'color': '#e74c3c'},
        {'nombre': 'profesionales', 'color': '#2c3e50'},
        {'nombre': 'cuadernos', 'color': '#f39c12'},
        {'nombre': 'escolares', 'color': '#27ae60'},
        {'nombre': 'oficina', 'color': '#8e44ad'},
        {'nombre': 'decoración', 'color': '#e67e22'},
        {'nombre': 'regalos', 'color': '#1abc9c'},
        {'nombre': 'personalizados', 'color': '#34495e'},
        {'nombre': 'premium', 'color': '#d35400'},
    ]
    
    print("Creando tags...")
    for tag_data in tags_data:
        tag, created = Tag.objects.get_or_create(
            nombre=tag_data['nombre'],
            defaults={'color': tag_data['color']}
        )
        if created:
            print(f"✓ Tag creado: {tag.nombre}")
        else:
            print(f"- Tag ya existe: {tag.nombre}")
    
    print("\n¡Tags creados exitosamente!")
    print("\nAhora puedes:")
    print("1. Ir al admin (/admin/)")
    print("2. Editar las categorías existentes")
    print("3. Asignar tags a las categorías")
    print("4. Asignar tags adicionales a los productos")

if __name__ == '__main__':
    crear_tags()