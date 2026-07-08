from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#6c757d', help_text='Color del tag en formato hex')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Tags"
        ordering = ['nombre']

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria_madre = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='subcategorias',
        help_text='Si esta es una subcategoría, selecciona la categoría principal'
    )
    tags = models.ManyToManyField(Tag, blank=True)
    visible_navegacion = models.BooleanField(default=True, help_text='¿Mostrar en el menú de navegación?')

    def __str__(self):
        if self.categoria_madre:
            return f'{self.categoria_madre.nombre} → {self.nombre}'
        return self.nombre

    def get_tags_display(self):
        return ' > '.join([tag.nombre for tag in self.tags.filter(activo=True)])

    class Meta:
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ManyToManyField(Categoria, blank=True, verbose_name='Categorías')
    tags_adicionales = models.ManyToManyField(Tag, blank=True, help_text='Tags adicionales para este producto')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, max_length=500)
    imagen_url = models.URLField(blank=True, null=True, help_text='URL externa de la imagen')
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Campos Google Shopping
    GOOGLE_CATEGORIES = [
        ('', '-- Seleccionar --'),
        ('5709', 'Artículos de Fiesta'),
        ('96', 'Sorpresas / Cotillón'),
        ('5710', 'Envoltorios de Regalo'),
        ('5711', 'Decoración de Fiestas'),
        ('5712', 'Banners y Guirnaldas'),
        ('5713', 'Invitaciones'),
        ('5714', 'Gorros de Fiesta'),
        ('536', 'Decoración del Hogar'),
        ('592', 'Velas Decorativas'),
        ('1876', 'Dulces y Chocolates'),
        ('1253', 'Juguetes'),
        ('3867', 'Puzzles'),
        ('4352', 'Peluches'),
        ('5593', 'Baby Shower'),
        ('923', 'Papelería'),
        ('5874', 'Tarjetas de Regalo'),
        ('5192', 'Disfraces y Accesorios'),
        ('505370', 'Manualidades'),
    ]
    marca = models.CharField(max_length=100, default='Mundo Magie', help_text='Marca del producto')
    mpn = models.CharField(max_length=100, blank=True, help_text='Número de parte del fabricante (único por producto)')
    google_category = models.CharField(max_length=300, blank=True, choices=GOOGLE_CATEGORIES, help_text='Categoría de Google Shopping')
    condicion = models.CharField(max_length=20, choices=[('new', 'Nuevo'), ('refurbished', 'Reacondicionado'), ('used', 'Usado')], default='new')
    sincronizar_google = models.BooleanField(default=True, help_text='¿Sincronizar con Google Shopping?')
    
    es_digital = models.BooleanField(default=False, help_text='¿Es un producto digital? Se enviará por correo electrónico.')
    archivo_digital = models.FileField(upload_to='digitales/', blank=True, null=True, help_text='Archivo a enviar por correo al comprar (PDF, ZIP, etc.)')
    
    # Campos de personalización
    permite_personalizacion = models.BooleanField(default=False, help_text='¿Este producto permite personalización?')
    texto_personalizacion = models.CharField(max_length=200, blank=True, help_text='Ej: ¿Quieres ponerle nombre personalizado?')
    placeholder_personalizacion = models.CharField(max_length=100, blank=True, help_text='Texto de ejemplo para el campo')
    
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import unicodedata
            base = slugify(unicodedata.normalize('NFKD', self.nombre))
            slug = base
            n = 1
            while Producto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def _imagen_principal(self):
        img = self.imagenes.filter(es_principal=True).first()
        if not img:
            img = self.imagenes.first()
        if img and img.imagen:
            return img.imagen
        if self.imagen:
            return self.imagen
        return None
    imagen_principal = property(_imagen_principal)
    
    def todas_las_imagenes(self):
        """Retorna todas las imágenes del producto para mostrar en el catálogo"""
        imagenes = []
        
        # Agregar todas las imágenes de ImagenProducto
        for img in self.imagenes.all():
            imagenes.append(img.imagen)
        
        # Si hay imagen individual y no está en ImagenProducto, agregarla
        if self.imagen:
            urls_existentes = [img.imagen.url for img in self.imagenes.all() if img.imagen]
            if self.imagen.url not in urls_existentes:
                imagenes.append(self.imagen)
        
        return imagenes
    
    @property
    def precio_desde(self):
        """Retorna el precio mínimo considerando variantes y opciones."""
        precios = [self.precio]
        for op in self.opciones.all():
            precios.append(op.precio)
        for attr in self.atributos.all():
            for val in attr.valores.filter(activo=True):
                if val.precio > 0:
                    precios.append(val.precio)
        return min(precios)

    @property
    def tiene_rango_precios(self):
        """True si hay variantes/opciones con precios distintos al base."""
        for attr in self.atributos.all():
            if attr.valores.filter(activo=True, precio__gt=0).exists():
                return True
        if self.opciones.exists():
            return True
        return False
    
    class Meta:
        ordering = ['-fecha_creacion']

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    def __str__(self):
        usuario_str = self.usuario.username if self.usuario else "Invitado"
        return f"Pedido #{self.id} - {usuario_str}"
    
    class Meta:
        ordering = ['-fecha']

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    personalizacion = models.TextField(blank=True, help_text='Texto de personalización del cliente')
    imagen_personalizacion = models.ImageField(upload_to='personalizaciones/', blank=True, null=True, help_text='Imagen subida por el cliente')
    
    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"

class Pago(models.Model):
    METODOS_PAGO = [
        ('flow', 'Flow'),
        ('mercadopago', 'MercadoPago'),
    ]
    
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('fallido', 'Fallido'),
        ('cancelado', 'Cancelado'),
    ]
    
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='pago')
    metodo = models.CharField(max_length=20, choices=METODOS_PAGO)
    estado = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    token_pago = models.CharField(max_length=200, blank=True)
    id_transaccion = models.CharField(max_length=200, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    datos_respuesta = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"Pago {self.id} - {self.pedido} - {self.estado}"
    
    class Meta:
        ordering = ['-fecha_creacion']

class ImagenInterior(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes_interior')
    imagen = models.ImageField(upload_to='interior/', max_length=500)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.producto.nombre} - Interior {self.orden}"

    class Meta:
        ordering = ['orden']
        verbose_name = "Imagen de Interior"
        verbose_name_plural = "Imágenes de Interior"


class Slide(models.Model):
    titulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to='slides/', max_length=500)
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Slide {self.orden} - {self.titulo}"
    
    class Meta:
        ordering = ['orden']

class ConfiguracionSitio(models.Model):
    mensaje_envio = models.CharField(max_length=200, default='Envíos a domicilio en 3 días hábiles')
    activo = models.BooleanField(default=True)
    
    # Colores del sitio
    color_primario = models.CharField(max_length=7, default='#495057', help_text='Color principal (botones, enlaces)')
    color_secundario = models.CharField(max_length=7, default='#6c757d', help_text='Color secundario (texto, bordes)')
    color_fondo = models.CharField(max_length=7, default='#f8f9fa', help_text='Color de fondo del sitio')
    color_banner = models.CharField(max_length=7, default='#28a745', help_text='Color del banner de envío')
    color_cards = models.CharField(max_length=7, default='#ffffff', help_text='Color de fondo de las cards')
    color_hover = models.CharField(max_length=7, default='#F4C2C2', help_text='Color de hover en navegación')
    
    def __str__(self):
        return "Configuración del Sitio"
    
    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuración del Sitio"

class SeccionCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    orden = models.IntegerField(default=1, help_text='Orden de aparición (1, 2, 3)')
    activo = models.BooleanField(default=True)
    # Split banner
    banner_imagen = models.ImageField(upload_to='banners/', blank=True, null=True, max_length=500, help_text='Imagen del banner izquierdo')
    banner_titulo = models.CharField(max_length=100, blank=True, default='', help_text='Título del banner (ej: Recién llegados)')
    banner_subtitulo = models.CharField(max_length=200, blank=True, default='', help_text='Subtítulo o descripción breve')
    banner_boton_texto = models.CharField(max_length=50, blank=True, default='Ver todo', help_text='Texto del botón CTA')

    def __str__(self):
        return f"Sección {self.orden} - {self.categoria.nombre if self.categoria else 'Sin categoría'}"

    class Meta:
        ordering = ['orden']
        verbose_name = "Sección de Categoría"
        verbose_name_plural = "Secciones de Categorías"

class BannerFidelizacion(models.Model):
    titulo = models.CharField(max_length=100, help_text='Ej: Creados con amor')
    descripcion = models.CharField(max_length=200, blank=True, help_text='Descripción breve del banner')
    icono = models.CharField(max_length=50, default='fas fa-heart', help_text='Clase de Font Awesome (ej: fas fa-heart, fas fa-shipping-fast)')
    color_icono = models.CharField(max_length=7, default='#495057', help_text='Color del ícono')
    color_texto = models.CharField(max_length=7, default='#6c757d', help_text='Color del texto')
    color_fondo = models.CharField(max_length=7, default='#ffffff', help_text='Color de fondo del banner')
    orden = models.IntegerField(default=0, help_text='Orden de aparición')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Banner de Fidelización"
        verbose_name_plural = "Banners de Fidelización"

class FooterConfig(models.Model):
    color_fondo = models.CharField(max_length=7, default='#2c3e50', help_text='Color de fondo del footer')
    color_texto = models.CharField(max_length=7, default='#ecf0f1', help_text='Color del texto')
    color_enlaces = models.CharField(max_length=7, default='#3498db', help_text='Color de los enlaces')
    color_hover = models.CharField(max_length=7, default='#aeefff', help_text='Color hover de enlaces')
    color_redes = models.CharField(max_length=7, default='#e74c3c', help_text='Color de los íconos de redes sociales')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return "Configuración del Footer"
    
    class Meta:
        verbose_name = "Configuración del Footer"
        verbose_name_plural = "Configuración del Footer"

class SobreMi(models.Model):
    titulo = models.CharField(max_length=100, default='Sobre Mí')
    contenido = models.TextField(help_text='Descripción sobre la tienda o propietario')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Sobre Mí"
        verbose_name_plural = "Sobre Mí"

class Contacto(models.Model):
    titulo = models.CharField(max_length=100, default='Contacto')
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    horarios = models.TextField(blank=True, help_text='Horarios de atención')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contacto"

class Informacion(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Información"
        verbose_name_plural = "Información"

class Suscripcion(models.Model):
    titulo = models.CharField(max_length=100, default='Suscríbete')
    descripcion = models.TextField(default='Recibe nuestras ofertas y novedades')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripción"

class RedSocial(models.Model):
    nombre = models.CharField(max_length=50)
    icono = models.CharField(max_length=50, help_text='Clase de Font Awesome (ej: fab fa-facebook)')
    url = models.URLField()
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/', max_length=500)
    orden = models.IntegerField(default=0)
    es_principal = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.producto.nombre} - Imagen {self.orden}"
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"

class VarianteAtributo(models.Model):
    """Ej: Talla, Color, Tamaño"""
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='atributos')
    nombre = models.CharField(max_length=100, help_text='Ej: Talla, Color, Material')
    valores_texto = models.CharField(
        max_length=500, blank=True,
        help_text='Escribe los valores separados por coma. Ej: S, M, L, XL'
    )
    orden = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.producto.nombre} — {self.nombre}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Sincronizar valores_texto con VarianteValor
        if self.valores_texto:
            valores_actuales = [v.strip() for v in self.valores_texto.split(',') if v.strip()]
            # Eliminar los que ya no están
            self.valores.exclude(valor__in=valores_actuales).delete()
            # Crear los nuevos
            existentes = set(self.valores.values_list('valor', flat=True))
            for i, val in enumerate(valores_actuales):
                if val not in existentes:
                    VarianteValor.objects.create(
                        atributo=self, valor=val, orden=i
                    )

    class Meta:
        ordering = ['orden']
        verbose_name = 'Variante'
        verbose_name_plural = 'Variantes del producto'


class VarianteValor(models.Model):
    atributo = models.ForeignKey(VarianteAtributo, on_delete=models.CASCADE, related_name='valores')
    valor = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Precio real de esta variante (ej: 15000, 18000). Si es 0, usa el precio base del producto.')
    stock = models.IntegerField(default=0)
    imagen_producto = models.ForeignKey(
        'ImagenProducto', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='variantes',
        help_text='Imagen del producto que se muestra al elegir esta variante'
    )
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    def get_precio(self):
        """Retorna el precio real: si tiene precio propio lo usa, si no usa el del producto."""
        if self.precio > 0:
            return self.precio
        return self.atributo.producto.precio

    def __str__(self):
        return f'{self.atributo.nombre}: {self.valor}'

    class Meta:
        ordering = ['orden']
        verbose_name = 'Valor de variante'
        verbose_name_plural = 'Valores de variantes'


class OpcionProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='opciones')
    nombre = models.CharField(max_length=200, help_text='Ej: 200 hojas')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}: ${self.precio}"
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Opción de Producto"
        verbose_name_plural = "Opciones de Producto"

class Descuento(models.Model):
    TIPO_CHOICES = [
        ('porcentaje', 'Porcentaje (%)'),
        ('monto', 'Monto fijo ($)'),
    ]
    APLICA_CHOICES = [
        ('producto', 'Producto específico'),
        ('categoria', 'Categoría'),
        ('todos', 'Todos los productos'),
    ]

    nombre = models.CharField(max_length=100, help_text='Nombre interno del descuento')
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True,
                              help_text='Cupón de descuento (opcional). Si no hay código, se aplica automáticamente.')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='porcentaje')
    valor = models.DecimalField(max_digits=10, decimal_places=2,
                                help_text='Ej: 10 para 10% o 1000 para $1000')
    aplica_a = models.CharField(max_length=20, choices=APLICA_CHOICES, default='todos')
    productos = models.ManyToManyField('Producto', blank=True,
                                       help_text='Productos con descuento (si aplica a producto específico)')
    categorias = models.ManyToManyField('Categoria', blank=True,
                                        help_text='Categorías con descuento')
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    usos_maximos = models.IntegerField(null=True, blank=True,
                                       help_text='Máximo de usos. Vacío = ilimitado')
    usos_actuales = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.nombre} ({self.valor}{"%" if self.tipo == "porcentaje" else "$"})'

    def es_valido(self):
        from django.utils import timezone
        hoy = timezone.now().date()
        if not self.activo:
            return False
        if self.fecha_inicio and hoy < self.fecha_inicio:
            return False
        if self.fecha_fin and hoy > self.fecha_fin:
            return False
        if self.usos_maximos and self.usos_actuales >= self.usos_maximos:
            return False
        return True

    def calcular_descuento(self, precio):
        if self.tipo == 'porcentaje':
            return round(float(precio) * float(self.valor) / 100, 2)
        return min(float(self.valor), float(precio))

    class Meta:
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
        ordering = ['-activo', 'nombre']


class ProyectoPortafolio(models.Model):
    CATEGORIAS = [
        ('landing', 'Landing Page'),
        ('ecommerce', 'Tienda Online'),
        ('dashboard', 'Dashboard'),
        ('linktree', 'Linktree / Bio Link'),
        ('corporativo', 'Sitio Corporativo'),
        ('otro', 'Otro'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='otro')
    imagen = models.ImageField(upload_to='portafolio/', blank=True, null=True)
    url_proyecto = models.URLField(blank=True, help_text='Link para ver el proyecto en vivo')
    tecnologias = models.CharField(max_length=200, blank=True, help_text='Ej: Django, Bootstrap, PostgreSQL')
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['orden', '-fecha_creacion']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Portafolio Web'


class Resena(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='resenas')
    nombre = models.CharField(max_length=100)
    puntuacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    aprobada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.producto.nombre} ({self.puntuacion}★)"

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"


class TokenDescarga(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    fecha_expiracion = models.DateTimeField()
    usado = models.BooleanField(default=False)

    def esta_vigente(self):
        from django.utils import timezone
        return not self.usado and timezone.now() < self.fecha_expiracion

    def __str__(self):
        return f'Token {self.token[:8]}... - {self.producto.nombre}'

    class Meta:
        verbose_name = 'Token de Descarga'
        verbose_name_plural = 'Tokens de Descarga'


class InstagramConfig(models.Model):
    usuario = models.CharField(max_length=100, help_text='Usuario de Instagram (sin @)')
    titulo = models.CharField(max_length=100, default='Síguenos en Instagram')
    mostrar_en_home = models.BooleanField(default=True)
    cantidad_posts = models.IntegerField(default=6, help_text='Cantidad de posts a mostrar')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Instagram: @{self.usuario}"
    
    class Meta:
        verbose_name = "Configuración de Instagram"
        verbose_name_plural = "Configuración de Instagram"