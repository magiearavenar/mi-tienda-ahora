import re
from django.http import HttpResponse
from django.conf import settings
from productos.models import Producto


def limpiar_texto(texto):
    """Elimina emojis y caracteres especiales no compatibles con XML."""
    if not texto:
        return ''
    # Eliminar emojis y símbolos
    texto = re.sub(r'[^\x00-\x7F\xC0-\xFF\u00C0-\u024F\u0400-\u04FF\s]', '', str(texto))
    # Limpiar espacios extra
    return texto.strip()


def google_feed_xml(request):
    """Feed XML compatible con Google Merchant Center."""
    base_url = settings.SITE_URL.rstrip('/')
    if not base_url.startswith('http'):
        base_url = f'https://{base_url}'
    productos = Producto.objects.filter(activo=True, sincronizar_google=True)

    items = []
    for p in productos:
        # Obtener URL de imagen
        imagen_url = ''
        if p.imagen_principal:
            img = p.imagen_principal
            imagen_url = img.url if hasattr(img, 'url') else ''
            if imagen_url and not imagen_url.startswith('http'):
                imagen_url = f'{base_url}{imagen_url}'
        elif p.imagen_url:
            imagen_url = p.imagen_url

        # Disponibilidad
        disponibilidad = 'in_stock' if p.stock > 0 else 'out_of_stock'

        # MPN: usar ID si no tiene
        mpn = p.mpn or f'MM-{p.id}'

        item = f'''    <item>
      <g:id>{p.id}</g:id>
      <g:title><![CDATA[{limpiar_texto(p.nombre)}]]></g:title>
      <g:description><![CDATA[{limpiar_texto(p.descripcion[:5000])}]]></g:description>
      <g:link>{base_url}/producto/{p.slug}/</g:link>
      <g:image_link>{imagen_url}</g:image_link>
      <g:availability>{disponibilidad}</g:availability>
      <g:price>{p.precio} CLP</g:price>
      <g:brand><![CDATA[{limpiar_texto(p.marca)}]]></g:brand>
      <g:mpn>{mpn}</g:mpn>
      <g:condition>{p.condicion}</g:condition>
      <g:shipping>
        <g:country>CL</g:country>
        <g:service>Standard</g:service>
        <g:price>0 CLP</g:price>
      </g:shipping>'''

        if p.google_category:
            item += f'\n      <g:google_product_category><![CDATA[{limpiar_texto(p.google_category)}]]></g:google_product_category>'

        # Imágenes adicionales
        for img in p.imagenes.all()[:10]:
            img_url = img.imagen.url if img.imagen else ''
            if img_url and not img_url.startswith('http'):
                img_url = f'{base_url}{img_url}'
            if img_url and img_url != imagen_url:
                item += f'\n      <g:additional_image_link>{img_url}</g:additional_image_link>'

        item += '\n    </item>'
        items.append(item)

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>Mundo Magie</title>
    <link>{base_url}</link>
    <description>Productos de Mundo Magie</description>
{chr(10).join(items)}
  </channel>
</rss>'''

    return HttpResponse(xml, content_type='application/xml')
