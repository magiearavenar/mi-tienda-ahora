from django.contrib import admin
from django import forms
from django.db import models
from .models import Producto, Categoria, Tag, Slide, ConfiguracionSitio, SeccionCategoria, BannerFidelizacion, FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, ImagenProducto, OpcionProducto, Pago, Pedido, DetallePedido, InstagramConfig, ProyectoPortafolio
from .widgets import ColorPickerWidget
from .image_widgets import DragDropImageWidget
# from .forms import ProductoAdminForm  # Comentado temporalmente

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color', 'activo']
    list_editable = ['color', 'activo']
    search_fields = ['nombre']
    list_filter = ['activo']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'visible_navegacion']
    list_editable = ['visible_navegacion']
    search_fields = ['nombre']
    list_filter = ['visible_navegacion']
    filter_horizontal = ['tags']

class ImagenProductoInline(admin.TabularInline):
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

    class Media:
        css = {'all': ('admin/css/dragdrop-image.css',)}
        js = ('admin/js/color-picker.js',)


class OpcionProductoInline(admin.TabularInline):
    model = OpcionProducto
    extra = 1
    fields = ['nombre', 'precio', 'orden']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'permite_personalizacion', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo', 'permite_personalizacion', 'fecha_creacion', 'tags_adicionales']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']
    inlines = [ImagenProductoInline, OpcionProductoInline]
    filter_horizontal = ['tags_adicionales']

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'precio', 'categoria', 'tags_adicionales', 'stock', 'activo')
        }),
        ('Imágenes', {
            'fields': ('imagen', 'imagen_url'),
        }),
        ('Personalización', {
            'fields': ('permite_personalizacion', 'texto_personalizacion', 'placeholder_personalizacion'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_bulk_upload'] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Procesar imágenes múltiples
        imagenes = request.FILES.getlist('imagenes_bulk')
        ultimo_orden = obj.imagenes.aggregate(
            max_orden=models.Max('orden')
        )['max_orden'] or 0
        for i, imagen in enumerate(imagenes):
            ImagenProducto.objects.create(
                producto=obj,
                imagen=imagen,
                orden=ultimo_orden + i + 1,
                es_principal=(i == 0 and not obj.imagenes.exists())
            )

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    ordering = ['orden']
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            kwargs['widget'] = DragDropImageWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)

class ConfiguracionSitioForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionSitio
        fields = '__all__'
        widgets = {
            'color_primario': ColorPickerWidget(),
            'color_secundario': ColorPickerWidget(),
            'color_fondo': ColorPickerWidget(),
            'color_banner': ColorPickerWidget(),
            'color_cards': ColorPickerWidget(),
            'color_hover': ColorPickerWidget(),
        }

@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    form = ConfiguracionSitioForm
    list_display = ['mensaje_envio', 'activo']
    list_editable = ['activo']
    fieldsets = (
        ('Mensaje', {
            'fields': ('mensaje_envio', 'activo')
        }),
        ('Colores del Sitio', {
            'fields': (('color_primario', 'color_secundario'), ('color_fondo', 'color_banner'), ('color_cards', 'color_hover')),
            'description': 'Haz clic en los cuadros de color para abrir el selector de colores. Los cambios se aplicarán inmediatamente en el sitio.'
        }),
    )
    
    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return True

class BannerFidelizacionForm(forms.ModelForm):
    class Meta:
        model = BannerFidelizacion
        fields = '__all__'
        widgets = {
            'color_icono': ColorPickerWidget(),
            'color_texto': ColorPickerWidget(),
            'color_fondo': ColorPickerWidget(),
        }

@admin.register(BannerFidelizacion)
class BannerFidelizacionAdmin(admin.ModelAdmin):
    form = BannerFidelizacionForm
    list_display = ['titulo', 'icono', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    ordering = ['orden']
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'descripcion', 'icono', 'orden', 'activo')
        }),
        ('Colores', {
            'fields': (('color_icono', 'color_texto'), 'color_fondo'),
            'description': 'Personaliza los colores del banner. Haz clic en los cuadros para abrir el selector de colores.'
        }),
    )
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',)
        }

class FooterConfigForm(forms.ModelForm):
    class Meta:
        model = FooterConfig
        fields = '__all__'
        widgets = {
            'color_fondo': ColorPickerWidget(),
            'color_texto': ColorPickerWidget(),
            'color_enlaces': ColorPickerWidget(),
            'color_hover': ColorPickerWidget(),
            'color_redes': ColorPickerWidget(),
        }

@admin.register(FooterConfig)
class FooterConfigAdmin(admin.ModelAdmin):
    form = FooterConfigForm
    list_display = ['color_fondo', 'activo']
    
    def has_add_permission(self, request):
        return not FooterConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(SobreMi)
class SobreMiAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'activo']
    fields = ['titulo', 'contenido', 'activo']
    
    def has_add_permission(self, request):
        return not SobreMi.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'telefono', 'email', 'activo']
    fields = ['titulo', 'telefono', 'email', 'direccion', 'horarios', 'activo']
    
    def has_add_permission(self, request):
        return not Contacto.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Informacion)
class InformacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    ordering = ['orden']

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'activo']
    fields = ['titulo', 'descripcion', 'activo']
    
    def has_add_permission(self, request):
        return not Suscripcion.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(RedSocial)
class RedSocialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono', 'url', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    ordering = ['orden']
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',)
        }

@admin.register(SeccionCategoria)
class SeccionCategoriaAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    list_filter = ['activo']
    ordering = ['orden']

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['producto', 'cantidad', 'precio', 'personalizacion']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'total', 'estado', 'fecha']
    list_filter = ['estado', 'fecha']
    search_fields = ['id', 'usuario__username']
    readonly_fields = ['fecha']
    inlines = [DetallePedidoInline]

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'metodo', 'estado', 'monto', 'fecha_creacion']
    list_filter = ['metodo', 'estado', 'fecha_creacion']
    search_fields = ['pedido__id', 'token_pago', 'id_transaccion']
    readonly_fields = ['fecha_creacion', 'fecha_pago', 'datos_respuesta']

@admin.register(ProyectoPortafolio)
class ProyectoPortafolioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'tecnologias', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    list_filter = ['categoria', 'activo']
    search_fields = ['titulo', 'descripcion']
    ordering = ['orden']
    fieldsets = (
        ('Información del Proyecto', {
            'fields': ('titulo', 'descripcion', 'categoria', 'tecnologias')
        }),
        ('Imagen y Link', {
            'fields': ('imagen', 'url_proyecto'),
        }),
        ('Configuración', {
            'fields': ('orden', 'activo'),
        }),
    )


@admin.register(InstagramConfig)
class InstagramConfigAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'titulo', 'mostrar_en_home', 'activo']
    list_editable = ['mostrar_en_home', 'activo']
    
    def has_add_permission(self, request):
        return not InstagramConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return True