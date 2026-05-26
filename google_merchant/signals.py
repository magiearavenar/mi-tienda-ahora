import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from productos.models import Producto

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Producto)
def sync_product_on_save(sender, instance, **kwargs):
    """Sincroniza producto con Google Merchant al guardar."""
    if not getattr(settings, 'GOOGLE_MERCHANT_ID', None):
        return
    if not instance.activo or not instance.sincronizar_google:
        return

    try:
        from google_merchant.api import sync_product
        sync_product(instance)
    except Exception as e:
        logger.error(f'Error auto-sync producto {instance.id}: {e}')


@receiver(post_delete, sender=Producto)
def delete_product_on_delete(sender, instance, **kwargs):
    """Elimina producto de Google Merchant al borrar."""
    if not getattr(settings, 'GOOGLE_MERCHANT_ID', None):
        return

    try:
        from google_merchant.api import delete_product
        delete_product(instance.id)
    except Exception as e:
        logger.error(f'Error eliminando producto {instance.id} de Google: {e}')
