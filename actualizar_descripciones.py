#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import BannerFidelizacion

# Actualizar banners con descripciones
descripciones = {
    'Creados con amor': 'Productos únicos hechos con dedicación',
    'Envío rápido': 'Entrega en 24-48 horas',
    'Calidad garantizada': '100% satisfacción asegurada',
    'Atención personalizada': 'Soporte dedicado para ti'
}

for titulo, descripcion in descripciones.items():
    try:
        banner = BannerFidelizacion.objects.get(titulo=titulo)
        banner.descripcion = descripcion
        banner.save()
        print(f"Banner '{titulo}' actualizado con descripción")
    except BannerFidelizacion.DoesNotExist:
        print(f"Banner '{titulo}' no encontrado")

print("¡Descripciones agregadas!")