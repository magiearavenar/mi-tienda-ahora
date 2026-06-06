from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, ImagenProducto
from .multi_image_widget import MultipleImageWidget
import json

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProductoAdminForm(forms.ModelForm):
    # Campo personalizado para múltiples imágenes
    imagenes_multiples = forms.FileField(
        widget=MultipleImageWidget(),
        required=False,
        help_text="Selecciona múltiples imágenes. Podrás configurar SKU, precios y orden para cada una."
    )
    
    # Campo oculto para datos adicionales de las imágenes
    imagenes_data = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        help_text="Datos adicionales de las imágenes (SKU, precio, orden)"
    )
    
    class Meta:
        model = Producto
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el campo imagen existente
        self.fields['imagen'].help_text = "Imagen principal del producto (opcional si usas imágenes múltiples)"
        self.fields['imagen'].required = False
    
    def save(self, commit=True):
        instance = super().save(commit)
        
        if commit:
            try:
                # Procesar las imágenes múltiples desde request.FILES
                request = getattr(self, '_request', None)
                if request and 'imagenes_multiples' in request.FILES:
                    imagenes_multiples = request.FILES.getlist('imagenes_multiples')
                    
                    if imagenes_multiples:
                        # Obtener datos adicionales de las imágenes
                        imagenes_data_raw = self.cleaned_data.get('imagenes_data', '{}')
                        try:
                            imagenes_data = json.loads(imagenes_data_raw) if imagenes_data_raw else {}
                        except (json.JSONDecodeError, TypeError):
                            imagenes_data = {}
                        
                        # Obtener el último orden para continuar la secuencia
                        ultimo_orden = 0
                        if instance.imagenes.exists():
                            ultimo_orden = instance.imagenes.aggregate(
                                max_orden=models.Max('orden')
                            )['max_orden'] or 0
                        
                        # Crear ImagenProducto para cada imagen subida
                        for i, imagen in enumerate(imagenes_multiples):
                            if imagen:  # Verificar que la imagen no esté vacía
                                try:
                                    # Obtener datos específicos de esta imagen
                                    img_data = imagenes_data.get(str(i), {})
                                    
                                    # Crear la imagen del producto
                                    imagen_producto = ImagenProducto.objects.create(
                                        producto=instance,
                                        imagen=imagen,
                                        orden=img_data.get('orden', ultimo_orden + i + 1),
                                        es_principal=img_data.get('es_principal', False) and i == 0
                                    )
                                    
                                    # Si tiene SKU o precio específico, crear OpcionProducto
                                    sku = img_data.get('sku', '').strip() if img_data.get('sku') else ''
                                    precio = img_data.get('precio')
                                    
                                    if sku or precio:
                                        from .models import OpcionProducto
                                        try:
                                            precio_final = float(precio) if precio else float(instance.precio)
                                            OpcionProducto.objects.create(
                                                producto=instance,
                                                nombre=sku or f"Opción {i+1}",
                                                precio=precio_final,
                                                orden=img_data.get('orden', ultimo_orden + i + 1)
                                            )
                                        except (ValueError, TypeError):
                                            # Si hay error con el precio, usar el precio base del producto
                                            OpcionProducto.objects.create(
                                                producto=instance,
                                                nombre=sku or f"Opción {i+1}",
                                                precio=instance.precio,
                                                orden=img_data.get('orden', ultimo_orden + i + 1)
                                            )
                                except Exception as e:
                                    # Log del error pero continúa procesando
                                    print(f"Error procesando imagen {i}: {e}")
                                    continue
            except Exception as e:
                # Log del error general pero no falla el guardado
                print(f"Error general procesando imágenes múltiples: {e}")
        
        return instance