import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import Categoria, Producto

print("=== CATEGORÍAS ===")
categorias = Categoria.objects.all()
print(f"Total categorías: {categorias.count()}")
for cat in categorias:
    print(f"- {cat.id}: {cat.nombre}")

print("\n=== PRODUCTOS ===")
productos = Producto.objects.all()
print(f"Total productos: {productos.count()}")
for prod in productos:
    categoria_nombre = prod.categoria.nombre if prod.categoria else "Sin categoría"
    print(f"- {prod.id}: {prod.nombre} (Categoría: {categoria_nombre}, Activo: {prod.activo})")

print("\n=== PRODUCTOS POR CATEGORÍA ===")
for cat in categorias:
    productos_cat = Producto.objects.filter(categoria=cat, activo=True)
    print(f"{cat.nombre}: {productos_cat.count()} productos activos")