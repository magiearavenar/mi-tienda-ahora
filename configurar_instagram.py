#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import InstagramConfig

def crear_configuracion_instagram():
    # Verificar si ya existe una configuración
    if InstagramConfig.objects.exists():
        print("Ya existe una configuración de Instagram.")
        config = InstagramConfig.objects.first()
        print(f"Usuario actual: @{config.usuario}")
        return
    
    # Crear configuración inicial
    config = InstagramConfig.objects.create(
        usuario='tu_usuario_instagram',
        titulo='Síguenos en Instagram',
        mostrar_en_home=True,
        cantidad_posts=6,
        activo=True
    )
    
    print("Configuracion de Instagram creada exitosamente!")
    print(f"Usuario: @{config.usuario}")
    print("Ve al panel de administración para cambiar el usuario de Instagram.")

if __name__ == '__main__':
    crear_configuracion_instagram()