from django.apps import AppConfig


class GoogleMerchantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'google_merchant'
    verbose_name = 'Google Merchant Center'

    def ready(self):
        import google_merchant.signals  # noqa
