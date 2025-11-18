#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import InstagramConfig

def actualizar_usuario_instagram():
    config = InstagramConfig.objects.first()
    if config:
        config.usuario = 'mundomagie.cl'
        config.save()
        print(f"Usuario de Instagram actualizado a: @{config.usuario}")
    else:
        # Crear nueva configuración
        config = InstagramConfig.objects.create(
            usuario='mundomagie.cl',
            titulo='Síguenos en Instagram',
            mostrar_en_home=True,
            cantidad_posts=6,
            activo=True
        )
        print(f"Configuración de Instagram creada con usuario: @{config.usuario}")

if __name__ == '__main__':
    actualizar_usuario_instagram()