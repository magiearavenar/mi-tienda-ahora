"""
Uso: python manage.py test_email_digital --email tu@email.com
"""
import os
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = 'Prueba el envio de email de descarga digital via Resend'

    def add_arguments(self, parser):
        parser.add_argument('--email', required=True, help='Email destino')

    def handle(self, *args, **options):
        import resend
        email = options['email']
        items = [{'nombre': 'Producto de prueba', 'url': 'https://www.mundomagie.cl/descargar/TOKEN_DE_PRUEBA/'}]

        try:
            html = render_to_string('emails/descarga_digital.html', {
                'nombre_usuario': 'Cliente de Prueba',
                'productos': items,
                'pedido': type('obj', (object,), {'id': 'TEST'})(),
            })

            resend.api_key = os.environ.get('RESEND_API_KEY', '')
            if not resend.api_key:
                self.stdout.write(self.style.ERROR('ERROR: RESEND_API_KEY no configurada'))
                return

            resend.Emails.send({
                'from': os.environ.get('RESEND_FROM_EMAIL', 'Mundo Magie <noreply@mundomagie.cl>'),
                'to': [email],
                'subject': '[TEST] Tu descarga digital - Mundo Magie',
                'html': html,
            })
            self.stdout.write(self.style.SUCCESS(f'OK - Email enviado correctamente a {email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'ERROR: {e}'))
