from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from .models import Producto, Categoria, Tag, Pedido, Slide, ConfiguracionSitio, SeccionCategoria, BannerFidelizacion, FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, ImagenProducto

def home(request):
    productos = Producto.objects.filter(activo=True).order_by('-fecha_creacion')[:8]
    categorias = Categoria.objects.filter(visible_navegacion=True)
    slides = Slide.objects.filter(activo=True)
    config = ConfiguracionSitio.objects.filter(activo=True).first()
    banners = BannerFidelizacion.objects.filter(activo=True)
    
    # Secciones de categorías
    secciones_categorias = SeccionCategoria.objects.filter(activo=True)[:3]
    secciones_con_productos = []
    
    for seccion in secciones_categorias:
        productos_seccion = Producto.objects.filter(
            categoria=seccion.categoria, 
            activo=True
        )[:12]  # 12 productos (6x2 filas)
        secciones_con_productos.append({
            'seccion': seccion,
            'productos': productos_seccion
        })
    
    return render(request, 'home.html', {
        'productos': productos,
        'categorias': categorias,
        'slides': slides,
        'config': config,
        'banners': banners,
        'secciones_categorias': secciones_con_productos
    })

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria, activo=True)
    categorias = Categoria.objects.filter(visible_navegacion=True)
    config = ConfiguracionSitio.objects.filter(activo=True).first()
    banners = BannerFidelizacion.objects.filter(activo=True)
    return render(request, 'productos.html', {
        'productos': productos,
        'categoria': categoria,
        'categorias': categorias,
        'config': config,
        'banners': banners
    })

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    categorias = Categoria.objects.filter(visible_navegacion=True)
    config = ConfiguracionSitio.objects.filter(activo=True).first()
    return render(request, 'detalle_producto.html', {'producto': producto, 'categorias': categorias, 'config': config})

def carrito(request):
    return render(request, 'carrito.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}')
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def perfil(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'perfil.html', {'pedidos': pedidos})

@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'detalle_pedido.html', {'pedido': pedido})

def buscar(request):
    query = request.GET.get('q', '')
    tag_query = request.GET.get('tag', '')
    productos = []
    categorias = Categoria.objects.filter(visible_navegacion=True)
    tags = Tag.objects.filter(activo=True)
    config = ConfiguracionSitio.objects.filter(activo=True).first()
    banners = BannerFidelizacion.objects.filter(activo=True)
    
    if query:
        productos = Producto.objects.filter(
            nombre__icontains=query,
            activo=True
        )
    elif tag_query:
        productos = Producto.objects.filter(
            tags_adicionales__nombre__icontains=tag_query,
            activo=True
        ).distinct()
    
    return render(request, 'buscar.html', {
        'productos': productos,
        'query': query,
        'tag_query': tag_query,
        'categorias': categorias,
        'tags': tags,
        'config': config,
        'banners': banners
    })

def productos_por_tag(request, tag_nombre):
    tag = get_object_or_404(Tag, nombre=tag_nombre, activo=True)
    productos = Producto.objects.filter(
        tags_adicionales=tag,
        activo=True
    ).distinct()
    categorias = Categoria.objects.filter(visible_navegacion=True)
    config = ConfiguracionSitio.objects.filter(activo=True).first()
    banners = BannerFidelizacion.objects.filter(activo=True)
    return render(request, 'productos.html', {
        'productos': productos,
        'tag': tag,
        'categorias': categorias,
        'config': config,
        'banners': banners
    })

def checkout(request):
    config = ConfiguracionSitio.objects.filter(activo=True).first()
    return render(request, 'checkout.html', {'config': config})

