#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial

# Crear configuración del footer
footer_config, created = FooterConfig.objects.get_or_create(
    defaults={
        'color_fondo': '#2c3e50',
        'color_texto': '#ecf0f1',
        'color_enlaces': '#3498db',
        'activo': True
    }
)
print(f"Footer Config: {'Creado' if created else 'Ya existe'}")

# Crear Sobre Mí
sobre_mi, created = SobreMi.objects.get_or_create(
    defaults={
        'titulo': 'Sobre Nosotros',
        'contenido': 'Somos una tienda dedicada a ofrecer productos únicos y de calidad. Cada artículo es seleccionado cuidadosamente para brindar la mejor experiencia a nuestros clientes.',
        'activo': True
    }
)
print(f"Sobre Mí: {'Creado' if created else 'Ya existe'}")

# Crear Contacto
contacto, created = Contacto.objects.get_or_create(
    defaults={
        'titulo': 'Contacto',
        'telefono': '+1 234 567 8900',
        'email': 'info@mundomagie.com',
        'direccion': 'Calle Principal 123, Ciudad',
        'horarios': 'Lun-Vie: 9:00-18:00',
        'activo': True
    }
)
print(f"Contacto: {'Creado' if created else 'Ya existe'}")

# Crear Información
info_items = [
    {'titulo': 'Política de Privacidad', 'contenido': 'Información sobre privacidad', 'orden': 1},
    {'titulo': 'Términos y Condiciones', 'contenido': 'Términos de uso', 'orden': 2},
    {'titulo': 'Política de Devoluciones', 'contenido': 'Información sobre devoluciones', 'orden': 3},
    {'titulo': 'Preguntas Frecuentes', 'contenido': 'FAQ', 'orden': 4}
]

for item in info_items:
    info, created = Informacion.objects.get_or_create(
        titulo=item['titulo'],
        defaults=item
    )
    print(f"Información '{item['titulo']}': {'Creado' if created else 'Ya existe'}")

# Crear Suscripción
suscripcion, created = Suscripcion.objects.get_or_create(
    defaults={
        'titulo': 'Newsletter',
        'descripcion': 'Suscríbete para recibir ofertas exclusivas y novedades',
        'activo': True
    }
)
print(f"Suscripción: {'Creado' if created else 'Ya existe'}")

# Crear Redes Sociales
redes_data = [
    {'nombre': 'Facebook', 'icono': 'fab fa-facebook', 'url': 'https://facebook.com', 'orden': 1},
    {'nombre': 'Instagram', 'icono': 'fab fa-instagram', 'url': 'https://instagram.com', 'orden': 2},
    {'nombre': 'Twitter', 'icono': 'fab fa-twitter', 'url': 'https://twitter.com', 'orden': 3},
    {'nombre': 'WhatsApp', 'icono': 'fab fa-whatsapp', 'url': 'https://wa.me/1234567890', 'orden': 4}
]

for red_data in redes_data:
    red, created = RedSocial.objects.get_or_create(
        nombre=red_data['nombre'],
        defaults=red_data
    )
    print(f"Red Social '{red_data['nombre']}': {'Creado' if created else 'Ya existe'}")

print("\n¡Footer configurado exitosamente!")