#!/usr/bin/env python
import os
import django
import sys

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from django.conf import settings

print("=== Configuración de Pagos ===")
print(f"FLOW_API_KEY: {'OK' if getattr(settings, 'FLOW_API_KEY', '') else 'FALTA'}")
print(f"FLOW_SECRET_KEY: {'OK' if getattr(settings, 'FLOW_SECRET_KEY', '') else 'FALTA'}")
print(f"FLOW_SANDBOX: {getattr(settings, 'FLOW_SANDBOX', 'No configurado')}")
print(f"MERCADOPAGO_ACCESS_TOKEN: {'OK' if getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', '') else 'FALTA'}")
print(f"MERCADOPAGO_SANDBOX: {getattr(settings, 'MERCADOPAGO_SANDBOX', 'No configurado')}")
print(f"SITE_URL: {getattr(settings, 'SITE_URL', 'No configurado')}")

# Probar servicios
try:
    from productos.services import FlowService
    flow = FlowService()
    print("OK FlowService inicializado correctamente")
except Exception as e:
    print(f"ERROR en FlowService: {e}")

try:
    from productos.services import MercadoPagoService
    mp = MercadoPagoService()
    print("OK MercadoPagoService inicializado correctamente")
except Exception as e:
    print(f"ERROR en MercadoPagoService: {e}")