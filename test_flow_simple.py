#!/usr/bin/env python
import requests
import hashlib

# Credenciales reales
api_key = "52354F01-C13D-4DC9-AAF7-6D6722L064A5"
secret_key = "cf8fab3737f51334aec56fdeb80aa57dfef133f8"

# Parámetros mínimos
params = {
    "apiKey": api_key,
    "commerceOrder": "TEST-001",
    "subject": "Test Payment",
    "amount": 1000,
    "email": "test@example.com",
    "urlConfirmation": "http://127.0.0.1:8000/flow/confirmar/",
    "urlReturn": "http://127.0.0.1:8000/pago/exitoso/"
}

# Crear firma según documentación Flow
cadena = f"{params['apiKey']}|{params['commerceOrder']}|{params['subject']}|{params['amount']}|{params['email']}|{params['urlConfirmation']}|{params['urlReturn']}"
params["s"] = hashlib.sha256((cadena + secret_key).encode()).hexdigest()

print("Cadena para firma:", cadena)
print("Firma generada:", params["s"])

# Probar con Flow producción
url = "https://www.flow.cl/api/payment/create"
response = requests.post(url, data=params)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    data = response.json()
    print("¡Éxito!")
    print(f"URL: {data.get('url')}?token={data.get('token')}")
else:
    print("Error en la respuesta")