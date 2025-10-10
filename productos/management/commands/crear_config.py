from django.core.management.base import BaseCommand
from productos.models import ConfiguracionSitio

class Command(BaseCommand):
    help = 'Crea configuración inicial del sitio'

    def handle(self, *args, **options):
        config, created = ConfiguracionSitio.objects.get_or_create(
            id=1,
            defaults={
                'mensaje_envio': 'Envíos a domicilio en 3 días hábiles',
                'activo': True
            }
        )
        
        if created:
            self.stdout.write('Configuración inicial creada')
        else:
            self.stdout.write('Configuración ya existe')