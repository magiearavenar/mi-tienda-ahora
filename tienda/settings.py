import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

# Jazzmin Admin Configuration
JAZZMIN_SETTINGS = {
    'site_title': 'Mundo Magie',
    'site_header': 'Mundo Magie',
    'site_brand': 'Mundo Magie',
    'site_logo': 'images/logo.png',
    'site_logo_classes': 'img-fluid',
    'site_icon': 'images/conf-ico.ico',
    'welcome_sign': 'Bienvenida al Panel de Administración',
    'copyright': 'Mundo Magie 2025',
    'search_model': ['productos.Producto', 'productos.Categoria'],
    'user_avatar': None,

    # Navbar
    'topmenu_links': [
        {'name': 'Ver Tienda', 'url': '/', 'new_window': True, 'icon': 'fas fa-store'},
        {'model': 'auth.user'},
    ],

    # Sidebar
    'show_sidebar': True,
    'navigation_expanded': True,
    'hide_apps': [],
    'hide_models': [],

    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',
        'productos.Producto': 'fas fa-box-open',
        'productos.Categoria': 'fas fa-tags',
        'productos.Tag': 'fas fa-tag',
        'productos.Pedido': 'fas fa-shopping-bag',
        'productos.Pago': 'fas fa-credit-card',
        'productos.Slide': 'fas fa-images',
        'productos.ConfiguracionSitio': 'fas fa-cog',
        'productos.BannerFidelizacion': 'fas fa-star',
        'productos.FooterConfig': 'fas fa-shoe-prints',
        'productos.SobreMi': 'fas fa-heart',
        'productos.Contacto': 'fas fa-envelope',
        'productos.Informacion': 'fas fa-info-circle',
        'productos.RedSocial': 'fas fa-share-alt',
        'productos.SeccionCategoria': 'fas fa-th-large',
        'productos.ImagenProducto': 'fas fa-camera',
        'productos.OpcionProducto': 'fas fa-list',
        'productos.InstagramConfig': 'fab fa-instagram',
    },

    'default_icon_parents': 'fas fa-folder',
    'default_icon_children': 'fas fa-circle',

    'related_modal_active': True,
    'custom_css': 'admin/css/jazzmin-custom.css',
    'custom_js': None,
    'use_google_fonts_cdn': True,
    'show_ui_builder': False,
    'changeform_format': 'horizontal_tabs',
    'changeform_format_overrides': {
        'auth.user': 'collapsible',
        'auth.group': 'vertical_tabs',
    },
    'language_chooser': False,
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': False,
    'body_small_text': False,
    'brand_small_text': False,
    'brand_colour': False,
    'accent': 'accent-pink',
    'navbar': 'navbar-white navbar-light',
    'no_navbar_border': True,
    'navbar_fixed': True,
    'layout_boxed': False,
    'footer_fixed': False,
    'sidebar_fixed': True,
    'sidebar': 'sidebar-light-pink',
    'sidebar_nav_small_text': False,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': True,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': False,
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },
}

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Railway production settings
if os.environ.get('RAILWAY_ENVIRONMENT'):
    DEBUG = False
    
# Logging para debug en producción
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }

ALLOWED_HOSTS = [
    'mundomagie.cl',
    'www.mundomagie.cl',
    '*.railway.app',
    '*.up.railway.app',
    '127.0.0.1',
    'localhost',
]

# Railway PORT
PORT = os.environ.get('PORT', 8000)

CSRF_TRUSTED_ORIGINS = [
    'https://mundomagie.cl',
    'https://www.mundomagie.cl',
    'https://*.railway.app',
    'https://*.up.railway.app',
]

# CSRF Settings
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Session security
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 3600  # 1 hora

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# HSTS (solo en producción)
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap4',
    'productos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'productos.middleware.AdminAccessMiddleware',
    'productos.middleware.RateLimitMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tienda.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'tienda/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'productos.context_processors.footer_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'tienda.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Configuración adicional para PostgreSQL en Railway
if 'postgresql' in DATABASES['default']['ENGINE']:
    DATABASES['default'].update({
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c default_transaction_isolation=serializable'
        },
        'CONN_MAX_AGE': 0,  # Desactivar pooling persistente
    })

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 10},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'tienda/static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Cloudinary Configuration (Reemplaza AWS S3)
if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    import cloudinary
    
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        secure=True
    )
    
    # Media files con Cloudinary
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
    
    # File upload settings
    FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
    DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
    
else:
    # Local media files (desarrollo)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Servir archivos estáticos con WhiteNoise en producción
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Configuración de pagos - Producción
FLOW_API_KEY = os.environ.get('FLOW_API_KEY', '')
FLOW_SECRET_KEY = os.environ.get('FLOW_SECRET_KEY', '')
FLOW_SANDBOX = os.environ.get('FLOW_SANDBOX', 'True').lower() == 'true'

MERCADOPAGO_ACCESS_TOKEN = os.environ.get('MERCADOPAGO_ACCESS_TOKEN', '')
MERCADOPAGO_SANDBOX = os.environ.get('MERCADOPAGO_SANDBOX', 'True').lower() == 'true'

SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')

# Instagram API
INSTAGRAM_ACCESS_TOKEN = os.environ.get('INSTAGRAM_ACCESS_TOKEN', '')