import os
import django
from dotenv import load_dotenv

load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

import cloudinary
from django.conf import settings

print("=== CLOUDINARY CONFIG ===")
print(f"Cloud Name: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
print(f"API Key: {os.environ.get('CLOUDINARY_API_KEY')}")
print(f"API Secret: {'***' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET'}")
print(f"Default Storage: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'NOT SET')}")

try:
    result = cloudinary.api.ping()
    print("✅ Cloudinary connection: SUCCESS")
    print(f"Status: {result}")
except Exception as e:
    print(f"❌ Cloudinary connection: FAILED")
    print(f"Error: {e}")