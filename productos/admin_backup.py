# Versión de respaldo del admin sin formulario personalizado
# Usar esta versión si hay problemas con el formulario personalizado

from django.contrib import admin
from django import forms
from .models import Producto, Categoria, Tag, Slide, ConfiguracionSitio, SeccionCategoria, BannerFidelizacion, FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, ImagenProducto, OpcionProducto, Pago, Pedido, DetallePedido, InstagramConfig
from .widgets import ColorPickerWidget
from .image_widgets import DragDropImageWidget

class ImagenProductoInlineSimple(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ['imagen', 'orden', 'es_principal', 'preview']
    readonly_fields = ['preview']
    
    def preview(self, obj):
        if obj.imagen:
            return f'<img src="{obj.imagen.url}" style="max-width: 100px; max-height: 100px; border-radius: 4px;">'
        return "Sin imagen"
    preview.short_description = "Vista previa"
    preview.allow_tags = True

class OpcionProductoInlineSimple(admin.TabularInline):
    model = OpcionProducto
    extra = 1
    fields = ['nombre', 'precio', 'orden']

@admin.register(Producto)
class ProductoAdminSimple(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'permite_personalizacion', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo', 'permite_personalizacion', 'fecha_creacion', 'tags_adicionales']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']
    inlines = [ImagenProductoInlineSimple, OpcionProductoInlineSimple]
    filter_horizontal = ['tags_adicionales']
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            kwargs['widget'] = DragDropImageWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'precio', 'categoria', 'tags_adicionales', 'stock', 'activo')
        }),
        ('Imágenes', {
            'fields': ('imagen', 'imagen_url'),
            'description': 'Imagen principal del producto. Usa "Imágenes de Productos" abajo para agregar más imágenes.'
        }),
        ('Personalización', {
            'fields': ('permite_personalizacion', 'texto_personalizacion', 'placeholder_personalizacion'),
            'description': 'Configura si este producto permite personalización y qué texto mostrar al cliente.'
        }),
    )