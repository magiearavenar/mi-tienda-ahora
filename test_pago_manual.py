#!/usr/bin/env python
import os
import django
import sys
import json

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import Producto, Pedido, DetallePedido

# Crear un pedido de prueba
print("=== Creando pedido de prueba ===")

# Obtener un producto
producto = Producto.objects.first()
if not producto:
    print("ERROR: No hay productos en la base de datos")
    exit(1)

print(f"Producto: {producto.nombre} - ${producto.precio}")

# Crear pedido
pedido = Pedido.objects.create(
    usuario=None,
    total=producto.precio,
    estado='pendiente'
)

# Crear detalle
DetallePedido.objects.create(
    pedido=pedido,
    producto=producto,
    cantidad=1,
    precio=producto.precio,
    personalizacion="Prueba de personalización"
)

print(f"Pedido creado: #{pedido.id}")

# Probar servicios de pago
try:
    from productos.services import MercadoPagoService
    mp_service = MercadoPagoService()
    url_mp = mp_service.crear_pago(pedido, "test@example.com")
    print(f"MercadoPago URL: {url_mp}")
except Exception as e:
    print(f"Error MercadoPago: {e}")

try:
    from productos.services import FlowService
    flow_service = FlowService()
    url_flow = flow_service.crear_pago(pedido, "test@example.com")
    print(f"Flow URL: {url_flow}")
except Exception as e:
    print(f"Error Flow: {e}")

print("=== Test completado ===")