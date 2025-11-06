from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check environment variables configuration'

    def handle(self, *args, **options):
        self.stdout.write('=== Environment Variables Check ===')
        
        vars_to_check = [
            'DEBUG',
            'FLOW_API_KEY',
            'FLOW_SECRET_KEY', 
            'FLOW_SANDBOX',
            'MERCADOPAGO_ACCESS_TOKEN',
            'MERCADOPAGO_SANDBOX',
            'SITE_URL',
            'RAILWAY_ENVIRONMENT'
        ]
        
        for var in vars_to_check:
            value = os.environ.get(var, 'NOT SET')
            if var in ['FLOW_SECRET_KEY', 'MERCADOPAGO_ACCESS_TOKEN']:
                # Ocultar valores sensibles
                display_value = 'SET' if value != 'NOT SET' else 'NOT SET'
            else:
                display_value = value
            
            self.stdout.write(f'{var}: {display_value}')
        
        self.stdout.write('\n=== Settings Values ===')
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        self.stdout.write(f'FLOW_SANDBOX: {getattr(settings, "FLOW_SANDBOX", "NOT SET")}')
        self.stdout.write(f'MERCADOPAGO_SANDBOX: {getattr(settings, "MERCADOPAGO_SANDBOX", "NOT SET")}')