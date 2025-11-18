# Configuración de Instagram API

## Para mostrar fotos reales de Instagram necesitas:

### 1. Crear una App en Facebook Developers
1. Ve a https://developers.facebook.com/
2. Crea una nueva app
3. Agrega el producto "Instagram Basic Display"

### 2. Configurar Instagram Basic Display
1. En tu app, ve a Instagram Basic Display > Basic Display
2. Crea un nuevo Instagram App ID
3. Agrega tu URL de redirect: `https://mundomagie.cl/`
4. Agrega usuarios de prueba (tu cuenta de Instagram)

### 3. Obtener el Access Token
1. Usa la herramienta de Graph API Explorer
2. O sigue el flujo de autorización manual
3. Necesitas el scope: `user_profile,user_media`

### 4. Agregar el token a tu proyecto
1. Copia el token de acceso
2. Agrégalo a tu archivo `.env`:
```
INSTAGRAM_ACCESS_TOKEN=tu_token_aqui
```

### 5. Alternativa Simple (Actual)
Por ahora, el sistema usa imágenes placeholder que simulan posts de Instagram.
Esto funciona perfectamente para mostrar la sección y el botón "Seguir".

## Notas Importantes:
- Los tokens de Instagram expiran cada 60 días
- Necesitas renovarlos periódicamente
- Para uso comercial, necesitas aprobación de Meta
- La implementación actual funciona sin API y es más simple de mantener