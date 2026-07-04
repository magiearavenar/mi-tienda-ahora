import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import Producto, Categoria
import shutil

DESTINO = '/app/media/digitales'
os.makedirs(DESTINO, exist_ok=True)

archivos = [f for f in os.listdir('/tmp/pdfs') if os.path.isfile(os.path.join('/tmp/pdfs', f))]
print(f"Encontrados {len(archivos)} archivos")

creados = 0
for nombre in archivos:
    origen = os.path.join('/tmp/pdfs', nombre)
    destino = os.path.join(DESTINO, nombre)
    # Evitar sobreescribir
    if os.path.exists(destino):
        base, ext = os.path.splitext(nombre)
        i = 1
        while os.path.exists(destino):
            destino = os.path.join(DESTINO, f'{base}_{i}{ext}')
            i += 1
    shutil.copy2(origen, destino)
    nombre_limpio = nombre.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').strip()
    ruta_relativa = 'digitales/' + os.path.basename(destino)
    if not Producto.objects.filter(archivo_digital=ruta_relativa).exists():
        p = Producto.objects.create(
            nombre=nombre_limpio,
            descripcion='',
            precio=0,
            stock=999,
            es_digital=True,
            activo=False,
        )
        Producto.objects.filter(pk=p.pk).update(archivo_digital=ruta_relativa)
        creados += 1
        print(f"✓ {nombre_limpio}")
    else:
        print(f"- Ya existe: {nombre_limpio}")

print(f"\n✅ {creados} productos creados.")
