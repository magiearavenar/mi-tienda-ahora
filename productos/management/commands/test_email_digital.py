"""
Uso: python manage.py test_email_digital --email tu@email.com [--pedido_id 1]
"""
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = 'Prueba el envio de email de descarga digital'

    def add_arguments(self, parser):
        parser.add_argument('--email', required=True, help='Email destino')
        parser.add_argument('--pedido_id', type=int, default=0)

    def handle(self, *args, **options):
        email = options['email']
        pedido_id = options['pedido_id']

        items = [{'nombre': 'Producto de prueba', 'url': 'https://www.mundomagie.cl/descargar/TOKEN_DE_PRUEBA/'}]

        try:
            html = render_to_string('emails/descarga_digital.html', {
                'nombre_usuario': 'Cliente de Prueba',
                'productos': items,
                'pedido': type('obj', (object,), {'id': pedido_id or 'TEST'})(),
            })
            msg = EmailMultiAlternatives(
                subject='[TEST] Tu descarga digital - Mundo Magie',
                body=f'Prueba de email. Link: {items[0]["url"]}',
                from_email=None,
                to=[email],
            )
            msg.attach_alternative(html, 'text/html')
            msg.send(fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f'OK - Email enviado correctamente a {email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'ERROR: {e}'))
