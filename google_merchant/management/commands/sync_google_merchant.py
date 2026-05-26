from django.core.management.base import BaseCommand
from google_merchant.api import sync_all_products


class Command(BaseCommand):
    help = 'Sincroniza todos los productos activos con Google Merchant Center'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando sincronización con Google Merchant Center...')
        results = sync_all_products()
        self.stdout.write(self.style.SUCCESS(
            f'Completado: {results["success"]} exitosos, {results["failed"]} fallidos'
        ))
