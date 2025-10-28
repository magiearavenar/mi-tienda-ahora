from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def robots_txt(request):
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /carrito/
Disallow: /checkout/

Sitemap: https://mundo-magie-production.up.railway.app/sitemap.xml"""
    return HttpResponse(content, content_type="text/plain")

def sitemap_xml(request):
    from productos.models import Producto, Categoria
    from datetime import datetime
    
    # Obtener el dominio actual
    domain = request.get_host()
    protocol = 'https' if request.is_secure() else 'http'
    base_url = f'{protocol}://{domain}'
    
    # Generar sitemap dinámico
    urls = []
    
    # Página principal
    urls.append(f'''
    <url>
        <loc>{base_url}/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>''')
    
    # Categorías
    for categoria in Categoria.objects.all():
        urls.append(f'''
    <url>
        <loc>{base_url}/categoria/{categoria.id}/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>''')
    
    # Productos
    for producto in Producto.objects.filter(activo=True):
        urls.append(f'''
    <url>
        <loc>{base_url}/producto/{producto.id}/</loc>
        <lastmod>{producto.fecha_creacion.strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>''')
    
    content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{''.join(urls)}
</urlset>'''
    
    return HttpResponse(content, content_type="application/xml")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap_xml),
    path('', include('productos.urls')),
]

# Servir archivos media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)