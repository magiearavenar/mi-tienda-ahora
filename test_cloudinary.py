import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    
    # Test Cloudinary connection
    print("Probando conexion con Cloudinary...")
    print(f"Cloud Name: {settings.CLOUDINARY_STORAGE['CLOUD_NAME']}")
    
    # Test API connection
    result = cloudinary.api.ping()
    print("Conexion exitosa con Cloudinary!")
    print(f"Status: {result.get('status', 'OK')}")
    
    # Test upload (opcional - crear imagen de prueba)
    print("\nProbando subida de imagen...")
    
    # Crear imagen de prueba simple
    from PIL import Image
    import io
    
    # Crear imagen de 100x100 pixeles
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Subir imagen de prueba
    upload_result = cloudinary.uploader.upload(
        img_bytes.getvalue(),
        public_id="test_image",
        folder="test"
    )
    
    print(f"Imagen subida exitosamente!")
    print(f"URL: {upload_result['secure_url']}")
    
    # Eliminar imagen de prueba
    cloudinary.uploader.destroy("test/test_image")
    print("Imagen de prueba eliminada")
    
except Exception as e:
    print(f"Error en la conexion: {e}")
    import traceback
    traceback.print_exc()