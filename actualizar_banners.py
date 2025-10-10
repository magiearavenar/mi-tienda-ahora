#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import BannerFidelizacion

# Actualizar banners con colores personalizados
banners_updates = [
    {
        'titulo': 'Creados con amor',
        'color_icono': '#e91e63',  # Rosa
        'color_texto': '#2c3e50',  # Azul oscuro
        'color_fondo': '#fce4ec'   # Rosa claro
    },
    {
        'titulo': 'Envío rápido',
        'color_icono': '#4caf50',  # Verde
        'color_texto': '#2c3e50',  # Azul oscuro
        'color_fondo': '#e8f5e8'   # Verde claro
    },
    {
        'titulo': 'Calidad garantizada',
        'color_icono': '#2196f3',  # Azul
        'color_texto': '#2c3e50',  # Azul oscuro
        'color_fondo': '#e3f2fd'   # Azul claro
    }
]

for banner_data in banners_updates:
    try:
        banner = BannerFidelizacion.objects.get(titulo=banner_data['titulo'])
        banner.color_icono = banner_data['color_icono']
        banner.color_texto = banner_data['color_texto']
        banner.color_fondo = banner_data['color_fondo']
        banner.save()
        print(f"Banner '{banner.titulo}' actualizado con colores personalizados")
    except BannerFidelizacion.DoesNotExist:
        print(f"Banner '{banner_data['titulo']}' no encontrado")

print("¡Banners actualizados con colores personalizados!")