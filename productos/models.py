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
    tags = models.ManyToManyField(Tag, blank=True, help_text='Tags asociados a esta categoría')
    visible_navegacion = models.BooleanField(default=True, help_text='¿Mostrar en el menú de navegación?')
    
    def __str__(self):
        return self.nombre
    
    def get_tags_display(self):
        return ' > '.join([tag.nombre for tag in self.tags.filter(activo=True)])
    
    class Meta:
        verbose_name_plural = "Categorías"

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    tags_adicionales = models.ManyToManyField(Tag, blank=True, help_text='Tags adicionales para este producto')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True, help_text='URL externa de la imagen')
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Campos de personalización
    permite_personalizacion = models.BooleanField(default=False, help_text='¿Este producto permite personalización?')
    texto_personalizacion = models.CharField(max_length=200, blank=True, help_text='Ej: ¿Quieres ponerle nombre personalizado?')
    placeholder_personalizacion = models.CharField(max_length=100, blank=True, help_text='Texto de ejemplo para el campo')
    
    def __str__(self):
        return self.nombre
    
    def imagen_principal(self):
        imagen_principal = self.imagenes.filter(es_principal=True).first()
        if imagen_principal:
            return imagen_principal.imagen
        primera_imagen = self.imagenes.first()
        if primera_imagen:
            return primera_imagen.imagen
        return self.imagen
    
    class Meta:
        ordering = ['-fecha_creacion']

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"
    
    class Meta:
        ordering = ['-fecha']

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    personalizacion = models.TextField(blank=True, help_text='Texto de personalización del cliente')
    
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

class Slide(models.Model):
    titulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to='slides/')
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
    
    def __str__(self):
        return f"Sección {self.orden} - {self.categoria.nombre}"
    
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
    imagen = models.ImageField(upload_to='productos/')
    orden = models.IntegerField(default=0)
    es_principal = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.producto.nombre} - Imagen {self.orden}"
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"

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