import mercadopago
from django.conf import settings
from django.urls import reverse
from .models import Pago, Pedido

class MercadoPagoService:
    def __init__(self):
        self.access_token = getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', '')
        self.sandbox = getattr(settings, 'MERCADOPAGO_SANDBOX', True)
        
        if not self.access_token or self.access_token.startswith('tu_mercadopago'):
            raise ValueError("MercadoPago credentials not configured")
            
        self.sdk = mercadopago.SDK(self.access_token)
    
    def crear_pago(self, pedido, email):
        try:
            preference_data = {
                "items": [
                    {
                        "title": f"Pedido #{pedido.id} - Mundo Magie",
                        "quantity": 1,
                        "unit_price": int(pedido.total),
                        "currency_id": "CLP"
                    }
                ],
                "payer": {
                    "email": email
                },
                "back_urls": {
                    "success": settings.SITE_URL + reverse('pago_exitoso'),
                    "failure": settings.SITE_URL + reverse('pago_fallido'),
                    "pending": settings.SITE_URL + reverse('pago_pendiente')
                },

                "external_reference": f"ORD-{pedido.id}",
                "notification_url": settings.SITE_URL + "/mercadopago/webhook/",

            }
            
            import logging
            logging.info(f"MP preference_data: {preference_data}")
            
            preference_response = self.sdk.preference().create(preference_data)
            
            logging.info(f"MP response: {preference_response}")
            
            if preference_response["status"] == 201:
                preference = preference_response["response"]
                
                # Crear registro de pago
                pago = Pago.objects.create(
                    pedido=pedido,
                    metodo='mercadopago',
                    monto=pedido.total,
                    token_pago=preference["id"]
                )
                
                if self.sandbox:
                    return preference["sandbox_init_point"]
                else:
                    return preference["init_point"]
            else:
                raise Exception(f"MercadoPago response error: {preference_response}")
                
        except Exception as e:
            raise Exception(f"MercadoPago service error: {str(e)}")
    
    def verificar_pago(self, payment_id):
        try:
            payment_response = self.sdk.payment().get(payment_id)
            
            if payment_response["status"] == 200:
                return payment_response["response"]
            else:
                raise Exception(f"MercadoPago payment verification error: {payment_response}")
                
        except Exception as e:
            raise Exception(f"MercadoPago verification error: {str(e)}")