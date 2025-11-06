#!/usr/bin/env python
import hashlib

# Credenciales de prueba
api_key = "52354F01-C13D-4DC9-AAF7-6D6722L064A5"
secret_key = "cf8fab3737f51334aec56fdeb80aa57dfef133f8"

# Parámetros de ejemplo
params = {
    "apiKey": api_key,
    "commerceOrder": "ORD-123",
    "subject": "Test",
    "amount": 1000,
    "email": "test@test.com",
    "urlConfirmation": "http://test.com/confirm",
    "urlReturn": "http://test.com/return"
}

print("=== Probando diferentes métodos de firma ===")

# Método 1: Orden alfabético
cadena1 = "|".join([str(params[k]) for k in sorted(params)])
firma1 = hashlib.sha256((cadena1 + secret_key).encode()).hexdigest()
print(f"Método 1 (alfabético): {cadena1}")
print(f"Firma 1: {firma1}")

# Método 2: Orden específico Flow
cadena2 = f"{params['apiKey']}|{params['commerceOrder']}|{params['subject']}|{params['amount']}|{params['email']}|{params['urlConfirmation']}|{params['urlReturn']}"
firma2 = hashlib.sha256((cadena2 + secret_key).encode()).hexdigest()
print(f"Método 2 (específico): {cadena2}")
print(f"Firma 2: {firma2}")

# Método 3: Solo valores en orden
cadena3 = f"{api_key}|ORD-123|Test|1000|test@test.com|http://test.com/confirm|http://test.com/return"
firma3 = hashlib.sha256((cadena3 + secret_key).encode()).hexdigest()
print(f"Método 3 (valores): {cadena3}")
print(f"Firma 3: {firma3}")