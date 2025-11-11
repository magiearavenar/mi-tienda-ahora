#!/usr/bin/env python
import os
import django
import sys

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')

try:
    django.setup()
    print("✓ Django setup OK")
    
    from django.conf import settings
    print(f"✓ DEBUG: {settings.DEBUG}")
    print(f"✓ DATABASE configured: {bool(settings.DATABASES)}")
    
    # Test database connection
    from django.db import connection
    connection.ensure_connection()
    print("✓ Database connection OK")
    
    # Test imports
    from productos.models import Producto
    print("✓ Models import OK")
    
    from productos.views import home
    print("✓ Views import OK")
    
    print("=== HEALTH CHECK PASSED ===")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)