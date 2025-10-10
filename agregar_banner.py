#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import BannerFidelizacion

# Agregar el cuarto banner
banner_data = {
    'titulo': 'Atención personalizada',
    'icono': 'fas fa-user-friends',
    'color_icono': '#9b59b6',  # Morado
    'color_texto': '#2c3e50',  # Azul oscuro
    'color_fondo': '#f3e5f5',  # Morado claro
    'orden': 4,
    'activo': True
}

banner, created = BannerFidelizacion.objects.get_or_create(
    titulo=banner_data['titulo'],
    defaults=banner_data
)

if created:
    print(f"Banner '{banner.titulo}' creado exitosamente")
else:
    print(f"Banner '{banner.titulo}' ya existe")

print("¡Cuarto banner agregado!")