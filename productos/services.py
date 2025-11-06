import hashlib
import requests
import mercadopago
from django.conf import settings
from django.urls import reverse
from .models import Pago, Pedido

class FlowService:
    def __init__(self):
        self.api_key = getattr(settings, 'FLOW_API_KEY', '')
        self.secret_key = getattr(settings, 'FLOW_SECRET_KEY', '')
        self.sandbox = getattr(settings, 'FLOW_SANDBOX', True)
        self.base_url = "https://sandbox.flow.cl/api" if self.sandbox else "https://www.flow.cl/api"
        
        if not self.api_key or not self.secret_key or self.secret_key.startswith('tu_flow'):
            raise ValueError("Flow credentials not configured")
    
    def crear_pago(self, pedido, email):
        try:
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
            
            # Crear firma - Flow requiere orden específico
            cadena = f"{params['apiKey']}|{params['commerceOrder']}|{params['subject']}|{params['amount']}|{params['email']}|{params['urlConfirmation']}|{params['urlReturn']}"
            params["s"] = hashlib.sha256((cadena + self.secret_key).encode()).hexdigest()
            
            response = requests.post(url, data=params, timeout=30)
            
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
                else:
                    raise Exception(f"Flow response error: {data}")
            else:
                raise Exception(f"Flow API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            raise Exception(f"Flow service error: {str(e)}")
    
    def verificar_pago(self, token):
        url = f"{self.base_url}/payment/getStatus"
        
        params = {
            "apiKey": self.api_key,
            "token": token
        }
        
        cadena = f"{params['apiKey']}|{params['token']}"
        params["s"] = hashlib.sha256((cadena + self.secret_key).encode()).hexdigest()
        
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            return response.json()
        
        return None

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

                "external_reference": f"ORD-{pedido.id}",

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