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
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://mundo-magie-production.up.railway.app/</loc>
        <lastmod>2025-01-01</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""
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