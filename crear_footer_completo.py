import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import SobreMi, Contacto, Informacion, Suscripcion, RedSocial

# Crear Sobre Mí
sobre_mi, created = SobreMi.objects.get_or_create(
    defaults={
        'titulo': 'Sobre Mí',
        'contenido': 'En Mundo Magie creamos productos únicos y especiales para hacer de cada momento algo mágico. Cada artículo está hecho con amor y dedicación para ti.',
        'activo': True
    }
)

# Crear Contacto
contacto, created = Contacto.objects.get_or_create(
    defaults={
        'titulo': 'Contacto',
        'telefono': '+56 9 1234 5678',
        'email': 'hola@mundomagie.cl',
        'direccion': 'Santiago, Chile',
        'horarios': 'Lun - Vie: 9:00 - 18:00',
        'activo': True
    }
)

# Crear Información
informaciones = [
    {'titulo': 'Política de Privacidad', 'contenido': 'Información sobre privacidad', 'orden': 1},
    {'titulo': 'Términos y Condiciones', 'contenido': 'Términos de uso', 'orden': 2},
    {'titulo': 'Envíos y Devoluciones', 'contenido': 'Información de envíos', 'orden': 3},
    {'titulo': 'Preguntas Frecuentes', 'contenido': 'FAQ', 'orden': 4},
]

for info_data in informaciones:
    Informacion.objects.get_or_create(
        titulo=info_data['titulo'],
        defaults={
            'contenido': info_data['contenido'],
            'orden': info_data['orden'],
            'activo': True
        }
    )

# Crear Suscripción
suscripcion, created = Suscripcion.objects.get_or_create(
    defaults={
        'titulo': 'Únete al Team Mundo Magie',
        'descripcion': 'Suscríbete y recibe ofertas exclusivas, novedades y contenido especial antes que nadie.',
        'activo': True
    }
)

# Crear Redes Sociales
redes = [
    {'nombre': 'TikTok', 'icono': 'fab fa-tiktok', 'url': 'https://tiktok.com/@mundomagie', 'orden': 1},
    {'nombre': 'Instagram', 'icono': 'fab fa-instagram', 'url': 'https://instagram.com/mundomagie', 'orden': 2},
    {'nombre': 'Facebook', 'icono': 'fab fa-facebook', 'url': 'https://facebook.com/mundomagie', 'orden': 3},
]

for red_data in redes:
    RedSocial.objects.get_or_create(
        nombre=red_data['nombre'],
        defaults={
            'icono': red_data['icono'],
            'url': red_data['url'],
            'orden': red_data['orden'],
            'activo': True
        }
    )

print("Footer completo creado exitosamente!")
print("- Sobre Mi: Creado")
print("- Contacto: Creado") 
print("- Informacion: 4 enlaces creados")
print("- Suscripcion: Team Mundo Magie creado")
print("- Redes Sociales: TikTok, Instagram, Facebook creados")