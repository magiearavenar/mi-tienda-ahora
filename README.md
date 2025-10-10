# Mi Tienda - Ecommerce Django

## Configuración

1. **Instalar Python** (3.8 o superior)

2. **Configurar el proyecto:**
   ```bash
   # Ejecutar el script de configuración
   setup.bat
   ```

3. **Iniciar el servidor:**
   ```bash
   python manage.py runserver
   ```

## Acceso

- **Tienda:** http://127.0.0.1:8000/
- **Panel Admin:** http://127.0.0.1:8000/admin/

## Funcionalidades

### Panel de Administración
- Login con usuario y contraseña
- Gestión de productos (crear, editar, eliminar)
- Gestión de categorías
- Control de stock
- Subida de imágenes

### Frontend
- Catálogo de productos
- Filtrado por categorías
- Carrito de compras (localStorage)
- Diseño responsive con Bootstrap

## Estructura del Proyecto

```
mi-tienda/
├── tienda/          # Configuración principal
├── productos/       # App de productos
├── media/          # Imágenes subidas
├── templates/      # Plantillas HTML
└── manage.py       # Comando Django
```

## Próximas Mejoras

- Sistema de pagos
- Gestión de usuarios
- Historial de pedidos
- Sistema de envíos