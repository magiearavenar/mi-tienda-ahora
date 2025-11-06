import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial

# Crear configuración del footer
footer_config, created = FooterConfig.objects.get_or_create(
    defaults={
        'color_fondo': '#f8f4ff',
        'color_texto': '#4a4a4a',
        'color_enlaces': '#d7b9ff',
        'color_hover': '#aeefff',
        'color_redes': '#ffc1e3',
        'activo': True
    }
)

# Crear Sobre Mí
sobre_mi, created = SobreMi.objects.get_or_create(
    defaults={
        'titulo': 'Sobre Mundo Magie',
        'contenido': 'Creamos productos únicos y mágicos con amor y dedicación. Cada artículo está diseñado para hacer de tus momentos algo especial.',
        'activo': True
    }
)

# Crear Contacto
contacto, created = Contacto.objects.get_or_create(
    defaults={
        'titulo': 'Contacto',
        'telefono': '+1 234 567 8900',
        'email': 'info@mundomagie.com',
        'direccion': 'Ciudad Mágica, País Encantado',
        'horarios': 'Lun-Vie: 9:00-18:00',
        'activo': True
    }
)

# Crear información
info_items = [
    'Política de Privacidad',
    'Términos y Condiciones',
    'Envíos y Devoluciones',
    'Preguntas Frecuentes'
]

for i, titulo in enumerate(info_items):
    Informacion.objects.get_or_create(
        titulo=titulo,
        defaults={
            'contenido': f'Contenido de {titulo}',
            'orden': i,
            'activo': True
        }
    )

# Crear suscripción
suscripcion, created = Suscripcion.objects.get_or_create(
    defaults={
        'titulo': 'Newsletter',
        'descripcion': 'Recibe nuestras ofertas y novedades directamente en tu email',
        'activo': True
    }
)

# Crear redes sociales
redes = [
    {'nombre': 'Instagram', 'icono': 'fab fa-instagram', 'url': 'https://instagram.com/mundomagie', 'orden': 1},
    {'nombre': 'Facebook', 'icono': 'fab fa-facebook', 'url': 'https://facebook.com/mundomagie', 'orden': 2},
    {'nombre': 'TikTok', 'icono': 'fab fa-tiktok', 'url': 'https://tiktok.com/@mundomagie', 'orden': 3}
]

for red in redes:
    RedSocial.objects.get_or_create(
        nombre=red['nombre'],
        defaults={
            'icono': red['icono'],
            'url': red['url'],
            'orden': red['orden'],
            'activo': True
        }
    )

print("Datos del footer creados exitosamente")