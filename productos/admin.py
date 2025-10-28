from django.contrib import admin
from django import forms
from .models import Producto, Categoria, Slide, ConfiguracionSitio, SeccionCategoria, BannerFidelizacion, FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, ImagenProducto, OpcionProducto
from .widgets import ColorPickerWidget

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ['imagen', 'orden', 'es_principal']

class OpcionProductoInline(admin.TabularInline):
    model = OpcionProducto
    extra = 1
    fields = ['nombre', 'precio', 'orden']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']
    inlines = [ImagenProductoInline, OpcionProductoInline]

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    ordering = ['orden']

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
        return False

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
        return False

@admin.register(SobreMi)
class SobreMiAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'activo']
    fields = ['titulo', 'contenido', 'activo']
    
    def has_add_permission(self, request):
        return not SobreMi.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'telefono', 'email', 'activo']
    fields = ['titulo', 'telefono', 'email', 'direccion', 'horarios', 'activo']
    
    def has_add_permission(self, request):
        return not Contacto.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

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
        return False

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