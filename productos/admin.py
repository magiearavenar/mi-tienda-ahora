from django.contrib import admin
from django import forms
from django.db import models
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.utils.html import format_html
from PIL import Image
import io
from .models import Producto, Categoria, Tag, Slide, ConfiguracionSitio, SeccionCategoria, BannerFidelizacion, FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, ImagenProducto, OpcionProducto, Pago, Pedido, DetallePedido, InstagramConfig, ProyectoPortafolio
from .widgets import ColorPickerWidget
from .image_widgets import DragDropImageWidget


def comprimir_imagen(imagen, max_kb=4000, max_px=1920):
    """Comprime una imagen a menos de max_kb KB y max_px px de ancho."""
    img = Image.open(imagen)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    # Redimensionar si es muy grande
    if img.width > max_px or img.height > max_px:
        img.thumbnail((max_px, max_px), Image.LANCZOS)
    # Comprimir hasta que quepa
    quality = 85
    while quality >= 40:
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        if buffer.tell() <= max_kb * 1024:
            break
        quality -= 10
    buffer.seek(0)
    nombre = imagen.name.rsplit('.', 1)[0] + '.jpg'
    return ContentFile(buffer.read(), name=nombre)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color', 'activo']
    list_editable = ['color', 'activo']
    search_fields = ['nombre']
    list_filter = ['activo']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria_madre', 'visible_navegacion']
    list_editable = ['visible_navegacion']
    list_filter = ['visible_navegacion', 'categoria_madre']
    search_fields = ['nombre']
    filter_horizontal = ['tags']

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 0
    fields = ['orden', 'imagen', 'es_principal', 'preview']
    readonly_fields = ['preview']
    ordering = ['orden']

    def preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width:80px;height:80px;object-fit:cover;border-radius:6px;border:2px solid #ddd;">',
                obj.imagen.url
            )
        return ''
    preview.short_description = 'Vista previa'

    class Media:
        css = {'all': ('admin/css/dragdrop-image.css', 'admin/css/inline-images.css')}
        js = ('admin/js/sortable-images.js',)


class OpcionProductoInline(admin.TabularInline):
    model = OpcionProducto
    extra = 1
    fields = ['nombre', 'precio', 'orden']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'mostrar_categoria', 'mostrar_tags', 'precio', 'stock', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo', 'permite_personalizacion', 'fecha_creacion', 'tags_adicionales']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']
    inlines = [ImagenProductoInline, OpcionProductoInline]
    filter_horizontal = ['tags_adicionales', 'categoria']
    actions = ['asignar_etiquetas', 'asignar_categoria']

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'precio', 'categoria', 'tags_adicionales', 'stock', 'activo')
        }),
        ('Personalización', {
            'fields': ('permite_personalizacion', 'texto_personalizacion', 'placeholder_personalizacion'),
        }),
    )

    def mostrar_categoria(self, obj):
        cats = obj.categoria.all()
        if not cats:
            return '-'
        html = ''
        for cat in cats:
            html += f'<span title="{cat.descripcion or cat.nombre}" style="background:#e8f4fd;color:#1a6fa8;padding:2px 8px;border-radius:10px;font-size:0.75rem;margin-right:3px;display:inline-block;">{cat.nombre}</span>'
        return format_html(html)
    mostrar_categoria.short_description = 'Categorías'
    mostrar_categoria.allow_tags = True

    def mostrar_tags(self, obj):
        tags = obj.tags_adicionales.filter(activo=True)
        if not tags:
            return '-'
        html = ''
        for tag in tags:
            html += f'<span title="Tag: {tag.nombre}" style="background:{tag.color};color:#fff;padding:2px 8px;border-radius:10px;font-size:0.75rem;margin-right:3px;display:inline-block;">{tag.nombre}</span>'
        return format_html(html)
    mostrar_tags.short_description = 'Etiquetas'
    mostrar_tags.allow_tags = True

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_bulk_upload'] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        imagenes = request.FILES.getlist('imagenes_bulk')
        ultimo_orden = obj.imagenes.aggregate(max_orden=models.Max('orden'))['max_orden'] or 0
        for i, imagen in enumerate(imagenes):
            try:
                imagen_comprimida = comprimir_imagen(imagen)
            except Exception:
                imagen_comprimida = imagen
            ImagenProducto.objects.create(
                producto=obj,
                imagen=imagen_comprimida,
                orden=ultimo_orden + i + 1,
                es_principal=(i == 0 and not obj.imagenes.filter(es_principal=True).exists())
            )

    def asignar_etiquetas(self, request, queryset):
        if 'aplicar' in request.POST:
            tag_ids = request.POST.getlist('tags_seleccionados')
            modo = request.POST.get('modo', 'agregar')
            tags = Tag.objects.filter(id__in=tag_ids)
            for producto in queryset:
                if modo == 'reemplazar':
                    producto.tags_adicionales.set(tags)
                else:
                    producto.tags_adicionales.add(*tags)
            self.message_user(request, f'Etiquetas asignadas a {queryset.count()} producto(s).')
            return
        return render(request, 'admin/asignar_etiquetas.html', {
            'productos': queryset,
            'tags': Tag.objects.filter(activo=True),
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        })
    asignar_etiquetas.short_description = '🏷️ Asignar etiquetas'

    def asignar_categoria(self, request, queryset):
        if 'aplicar' in request.POST:
            cat_id = request.POST.get('categoria_seleccionada')
            modo = request.POST.get('modo', 'agregar')
            if cat_id:
                categoria = Categoria.objects.get(id=cat_id)
                for producto in queryset:
                    if modo == 'reemplazar':
                        producto.categoria.set([categoria])
                    else:
                        producto.categoria.add(categoria)
                self.message_user(request, f'Categoría asignada a {queryset.count()} producto(s).')
            return
        return render(request, 'admin/asignar_categoria.html', {
            'productos': queryset,
            'categorias': Categoria.objects.all(),
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        })
    asignar_categoria.short_description = '📂 Asignar categoría'

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