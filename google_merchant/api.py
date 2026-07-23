import json
import logging
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from django.conf import settings
from productos.models import Producto

logger = logging.getLogger(__name__)

API_BASE = 'https://merchantapi.googleapis.com/products/v1beta'
SCOPES = ['https://www.googleapis.com/auth/content']


def get_session():
    """Obtiene sesión autenticada con credenciales de servicio."""
    credentials_value = getattr(settings, 'GOOGLE_MERCHANT_CREDENTIALS', None)
    if not credentials_value:
        raise ValueError('GOOGLE_MERCHANT_CREDENTIALS no configurado en settings.py')

    # Soporta tanto JSON directo como ruta de archivo
    try:
        info = json.loads(credentials_value)
        credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    except (json.JSONDecodeError, ValueError):
        credentials = service_account.Credentials.from_service_account_file(credentials_value, scopes=SCOPES)

    return AuthorizedSession(credentials)


def build_product_data(producto, base_url):
    """Construye el payload del producto para la API Merchant."""
    # Imagen principal
    imagen_url = ''
    if producto.imagen_principal:
        img = producto.imagen_principal
        imagen_url = img.url if hasattr(img, 'url') else ''
        if imagen_url and not imagen_url.startswith('http'):
            imagen_url = f'{base_url}{imagen_url}'
    elif producto.imagen_url:
        imagen_url = producto.imagen_url

    mpn = producto.mpn or f'MM-{producto.id}'

    data = {
        'channel': 'ONLINE',
        'offerId': str(producto.id),
        'contentLanguage': 'es',
        'feedLabel': 'CL',
        'attributes': {
            'title': producto.nombre,
            'description': producto.descripcion[:5000],
            'link': f'{base_url}/producto/{producto.slug}/',
            'imageLink': imagen_url,
            'availability': 'in_stock' if (producto.stock > 0 or producto.es_digital) else 'out_of_stock',
            'price': {
                'amountMicros': str(int(producto.precio * 1_000_000)),
                'currencyCode': 'CLP'
            },
            'brand': producto.marca,
            'mpn': mpn,
            'condition': producto.condicion,
        }
    }

    if producto.google_category:
        data['attributes']['googleProductCategory'] = producto.google_category

    # Imágenes adicionales
    additional = []
    for img in producto.imagenes.all()[:10]:
        img_url = img.imagen.url if img.imagen else ''
        if img_url and not img_url.startswith('http'):
            img_url = f'{base_url}{img_url}'
        if img_url and img_url != imagen_url:
            additional.append(img_url)
    if additional:
        data['attributes']['additionalImageLinks'] = additional

    return data


def sync_product(producto):
    """Sincroniza un producto con Google Merchant Center."""
    merchant_id = getattr(settings, 'GOOGLE_MERCHANT_ID', None)
    if not merchant_id:
        logger.warning('GOOGLE_MERCHANT_ID no configurado')
        return False

    base_url = settings.SITE_URL.rstrip('/')
    session = get_session()
    data = build_product_data(producto, base_url)

    url = f'{API_BASE}/accounts/{merchant_id}/productInputs:insert'
    params = {'dataSource': f'accounts/{merchant_id}/dataSources/primary'}

    response = session.post(url, json=data, params=params)

    if response.status_code in (200, 201):
        logger.info(f'Producto {producto.id} sincronizado con Google Merchant')
        return True
    else:
        logger.error(f'Error sincronizando producto {producto.id}: {response.status_code} - {response.text}')
        return False


def delete_product(producto_id):
    """Elimina un producto de Google Merchant Center."""
    merchant_id = getattr(settings, 'GOOGLE_MERCHANT_ID', None)
    if not merchant_id:
        return False

    session = get_session()
    name = f'accounts/{merchant_id}/productInputs/online~es~CL~{producto_id}'
    params = {'dataSource': f'accounts/{merchant_id}/dataSources/primary'}

    response = session.delete(f'{API_BASE}/{name}', params=params)
    return response.status_code in (200, 204)


def sync_all_products():
    """Sincroniza todos los productos activos."""
    productos = Producto.objects.filter(activo=True, sincronizar_google=True)
    results = {'success': 0, 'failed': 0}

    for producto in productos:
        if sync_product(producto):
            results['success'] += 1
        else:
            results['failed'] += 1

    return results
