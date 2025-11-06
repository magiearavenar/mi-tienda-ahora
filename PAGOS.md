# Configuración de Pasarelas de Pago

## Flow (Chile)

### 1. Crear cuenta en Flow
- Registrarse en https://www.flow.cl/
- Solicitar habilitación de API
- Obtener API Key y Secret Key

### 2. Configurar credenciales
En el archivo `.env`:
```
FLOW_API_KEY=tu_api_key_real
FLOW_SECRET_KEY=tu_secret_key_real
FLOW_SANDBOX=True  # False para producción
```

### 3. URLs de prueba
- Sandbox: https://sandbox.flow.cl/api
- Producción: https://www.flow.cl/api

## MercadoPago

### 1. Crear cuenta en MercadoPago
- Registrarse en https://www.mercadopago.cl/
- Ir a "Tus integraciones" > "Credenciales"
- Obtener Access Token

### 2. Configurar credenciales
En el archivo `.env`:
```
MERCADOPAGO_ACCESS_TOKEN=tu_access_token_real
MERCADOPAGO_SANDBOX=True  # False para producción
```

### 3. Webhooks
Para recibir notificaciones de pago, configurar webhook en:
- URL: https://tu-dominio.com/mercadopago/webhook/
- Eventos: payment

## Configuración del sitio

En el archivo `.env`:
```
SITE_URL=https://tu-dominio.com  # Para producción
SITE_URL=http://127.0.0.1:8000   # Para desarrollo
```

## Flujo de pago

1. Cliente llena carrito y datos de envío
2. Selecciona método de pago (Flow o MercadoPago)
3. Sistema crea pedido y redirige a pasarela
4. Cliente paga en la pasarela externa
5. Pasarela confirma pago via webhook
6. Sistema actualiza estado del pedido

## Estados de pago

- **pendiente**: Pago iniciado pero no confirmado
- **pagado**: Pago confirmado exitosamente
- **fallido**: Pago rechazado o falló
- **cancelado**: Pago cancelado por el usuario

## URLs importantes

- `/procesar-pago/` - Procesa el pago y redirige a pasarela
- `/flow/confirmar/` - Webhook para confirmación de Flow
- `/mercadopago/webhook/` - Webhook para confirmación de MercadoPago
- `/pago/exitoso/` - Página de pago exitoso
- `/pago/fallido/` - Página de pago fallido
- `/pago/pendiente/` - Página de pago pendiente

## Personalización de productos

Los productos con personalización se manejan automáticamente:
- Se guarda el texto personalizado en `DetallePedido.personalizacion`
- Se muestra en el carrito y en el admin
- Productos con diferente personalización se tratan como items separados