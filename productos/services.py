import hashlib
import requests
import mercadopago
from django.conf import settings
from django.urls import reverse
from .models import Pago, Pedido

class FlowService:
    def __init__(self):
        self.api_key = settings.FLOW_API_KEY
        self.secret_key = settings.FLOW_SECRET_KEY
        self.sandbox = settings.FLOW_SANDBOX
        self.base_url = "https://sandbox.flow.cl/api" if self.sandbox else "https://www.flow.cl/api"
    
    def crear_pago(self, pedido, email):
        url = f"{self.base_url}/payment/create"
        
        params = {
            "apiKey": self.api_key,
            "commerceOrder": f"ORD-{pedido.id}",
            "subject": f"Pedido #{pedido.id} - Mundo Magie",
            "amount": int(pedido.total),
            "email": email,
            "urlConfirmation": settings.SITE_URL + reverse('flow_confirmar'),
            "urlReturn": settings.SITE_URL + reverse('pago_exitoso'),
        }
        
        # Crear firma
        cadena = "|".join([str(params[k]) for k in sorted(params)])
        params["s"] = hashlib.sha256((cadena + self.secret_key).encode()).hexdigest()
        
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'url' in data and 'token' in data:
                # Crear registro de pago
                pago = Pago.objects.create(
                    pedido=pedido,
                    metodo='flow',
                    monto=pedido.total,
                    token_pago=data['token']
                )
                return data['url'] + "?token=" + data['token']
        
        return None
    
    def verificar_pago(self, token):
        url = f"{self.base_url}/payment/getStatus"
        
        params = {
            "apiKey": self.api_key,
            "token": token
        }
        
        cadena = "|".join([str(params[k]) for k in sorted(params)])
        params["s"] = hashlib.sha256((cadena + self.secret_key).encode()).hexdigest()
        
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            return response.json()
        
        return None

class MercadoPagoService:
    def __init__(self):
        self.access_token = settings.MERCADOPAGO_ACCESS_TOKEN
        self.sandbox = settings.MERCADOPAGO_SANDBOX
        self.sdk = mercadopago.SDK(self.access_token)
    
    def crear_pago(self, pedido, email):
        preference_data = {
            "items": [
                {
                    "title": f"Pedido #{pedido.id} - Mundo Magie",
                    "quantity": 1,
                    "unit_price": float(pedido.total),
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
            "auto_return": "approved",
            "external_reference": f"ORD-{pedido.id}",
            "notification_url": settings.SITE_URL + reverse('mercadopago_webhook')
        }
        
        preference_response = self.sdk.preference().create(preference_data)
        
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
        
        return None
    
    def verificar_pago(self, payment_id):
        payment_response = self.sdk.payment().get(payment_id)
        
        if payment_response["status"] == 200:
            return payment_response["response"]
        
        return None