#!/usr/bin/env python3
"""
Script para configurar Cloudinary como proveedor de imágenes
Reemplaza AWS S3 con una alternativa gratuita
"""

import os
import subprocess
import sys

def install_cloudinary():
    """Instala django-cloudinary-storage"""
    print("📦 Instalando django-cloudinary-storage...")
    subprocess.run([sys.executable, "-m", "pip", "install", "django-cloudinary-storage"], check=True)
    print("✅ django-cloudinary-storage instalado")

def update_requirements():
    """Actualiza requirements.txt"""
    requirements_path = "requirements.txt"
    
    # Leer requirements actuales
    with open(requirements_path, 'r') as f:
        lines = f.readlines()
    
    # Agregar cloudinary si no existe
    cloudinary_line = "django-cloudinary-storage==0.3.0\n"
    if not any("django-cloudinary-storage" in line for line in lines):
        lines.append(cloudinary_line)
    
    # Escribir requirements actualizados
    with open(requirements_path, 'w') as f:
        f.writelines(lines)
    
    print("✅ requirements.txt actualizado")

def create_env_template():
    """Crea template para variables de Cloudinary"""
    env_content = """
# Cloudinary Configuration (Reemplaza AWS S3)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key  
CLOUDINARY_API_SECRET=tu-api-secret
"""
    
    with open(".env.cloudinary", 'w') as f:
        f.write(env_content)
    
    print("✅ Archivo .env.cloudinary creado")

def show_instructions():
    """Muestra instrucciones para completar la configuración"""
    print("\n" + "="*60)
    print("🚀 CONFIGURACIÓN DE CLOUDINARY")
    print("="*60)
    print("\n1. Ve a: https://cloudinary.com/users/register/free")
    print("2. Crea una cuenta gratuita")
    print("3. En tu Dashboard, copia:")
    print("   - Cloud Name")
    print("   - API Key") 
    print("   - API Secret")
    print("\n4. Agrega estas variables a tu archivo .env:")
    print("   CLOUDINARY_CLOUD_NAME=tu-cloud-name")
    print("   CLOUDINARY_API_KEY=tu-api-key")
    print("   CLOUDINARY_API_SECRET=tu-api-secret")
    print("\n5. Ejecuta: python configure_cloudinary.py")
    print("\n💡 Límites gratuitos:")
    print("   - 25GB almacenamiento")
    print("   - 25GB ancho de banda/mes")
    print("   - Transformaciones ilimitadas")

if __name__ == "__main__":
    try:
        install_cloudinary()
        update_requirements()
        create_env_template()
        show_instructions()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)