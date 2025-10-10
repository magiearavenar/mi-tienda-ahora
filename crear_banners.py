#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import BannerFidelizacion

# Crear banners de ejemplo
banners_data = [
    {
        'titulo': 'Creados con amor',
        'icono': 'fas fa-heart',
        'orden': 1
    },
    {
        'titulo': 'Envío rápido',
        'icono': 'fas fa-shipping-fast',
        'orden': 2
    },
    {
        'titulo': 'Calidad garantizada',
        'icono': 'fas fa-shield-alt',
        'orden': 3
    }
]

for banner_data in banners_data:
    banner, created = BannerFidelizacion.objects.get_or_create(
        titulo=banner_data['titulo'],
        defaults=banner_data
    )
    if created:
        print(f"Banner '{banner.titulo}' creado exitosamente")
    else:
        print(f"Banner '{banner.titulo}' ya existe")

print("¡Banners de fidelización configurados!")