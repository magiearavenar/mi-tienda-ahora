from django import template
import re

register = template.Library()

@register.filter
def cloudinary_opt(url, params='f_auto,q_auto:good,w_auto'):
    """
    Transforma una URL de Cloudinary para agregar optimización automática.
    Uso: {{ imagen.url|cloudinary_opt }}
    Con tamaño: {{ imagen.url|cloudinary_opt:'f_auto,q_auto,w_800' }}
    """
    if not url:
        return url
    if 'res.cloudinary.com' not in str(url):
        return url
    url = str(url)
    # Si ya tiene transformaciones, no duplicar
    if '/f_auto' in url or '/q_auto' in url:
        return url
    # Insertar transformaciones antes de /upload/
    return re.sub(r'/upload/', f'/upload/{params}/', url, count=1)

@register.filter
def cloudinary_thumb(url):
    """Thumbnail pequeño para miniaturas — 200px, calidad buena"""
    return cloudinary_opt(url, 'f_auto,q_auto:good,w_200,h_200,c_fill')

@register.filter
def cloudinary_card(url):
    """Imagen para cards de productos — 400px"""
    return cloudinary_opt(url, 'f_auto,q_auto:good,w_400,h_400,c_pad')

@register.filter
def cloudinary_banner(url):
    """Imagen para banners — 800px"""
    return cloudinary_opt(url, 'f_auto,q_auto:good,w_800')
