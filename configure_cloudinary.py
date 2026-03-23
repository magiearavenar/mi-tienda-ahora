#!/usr/bin/env python3
"""
Script para configurar Cloudinary en settings.py
"""

import os
import re

def update_settings():
    """Actualiza settings.py para usar Cloudinary"""
    
    settings_path = "tienda/settings.py"
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar import de cloudinary
    if 'import cloudinary' not in content:
        content = content.replace(
            'from dotenv import load_dotenv',
            'from dotenv import load_dotenv\nimport cloudinary\nimport cloudinary.uploader\nimport cloudinary.api'
        )
    
    # Agregar cloudinary_storage a INSTALLED_APPS
    if 'cloudinary_storage' not in content:
        content = re.sub(
            r"INSTALLED_APPS = \[(.*?)'productos',",
            r"INSTALLED_APPS = [\1'cloudinary_storage',\n    'cloudinary',\n    'produtos',",
            content,
            flags=re.DOTALL
        )
    
    # Reemplazar configuración de AWS S3 con Cloudinary
    cloudinary_config = '''
# Cloudinary Configuration (Reemplaza AWS S3)
if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    import cloudinary
    
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        secure=True
    )
    
    # Media files con Cloudinary
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
    
    # File upload settings
    FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
    DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
    
else:
    # Local media files (desarrollo)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
'''
    
    # Buscar y reemplazar la configuración de AWS S3
    aws_pattern = r'# AWS S3 Configuration.*?else:\s*# Local media files.*?MEDIA_ROOT = BASE_DIR / \'media\''
    
    if re.search(aws_pattern, content, re.DOTALL):
        content = re.sub(aws_pattern, cloudinary_config.strip(), content, flags=re.DOTALL)
    else:
        # Si no encuentra el patrón, agregar al final antes de DEFAULT_AUTO_FIELD
        content = content.replace(
            "DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'",
            cloudinary_config + "\nDEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'"
        )
    
    # Escribir archivo actualizado
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ settings.py actualizado para usar Cloudinary")

def update_env_example():
    """Actualiza .env.example con variables de Cloudinary"""
    
    env_example_path = ".env.example"
    
    with open(env_example_path, 'r') as f:
        content = f.read()
    
    # Reemplazar AWS con Cloudinary
    content = re.sub(
        r'# AWS S3.*?AWS_S3_REGION_NAME=us-east-1',
        '''# Cloudinary (Reemplaza AWS S3)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret''',
        content,
        flags=re.DOTALL
    )
    
    with open(env_example_path, 'w') as f:
        f.write(content)
    
    print("✅ .env.example actualizado")

def show_next_steps():
    """Muestra los siguientes pasos"""
    print("\n" + "="*50)
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print("="*50)
    print("\n📋 Próximos pasos:")
    print("1. Crea cuenta en Cloudinary: https://cloudinary.com/users/register/free")
    print("2. Agrega las credenciales a tu .env")
    print("3. Ejecuta: python manage.py collectstatic")
    print("4. Reinicia el servidor: python manage.py runserver")
    print("\n💡 Beneficios de Cloudinary:")
    print("- ✅ 25GB gratis (vs 5GB de AWS)")
    print("- ✅ Optimización automática de imágenes")
    print("- ✅ CDN global incluido")
    print("- ✅ Redimensionado automático")

if __name__ == "__main__":
    try:
        update_settings()
        update_env_example()
        show_next_steps()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()