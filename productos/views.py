from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import models
import json
import requests
import os
from .models import Producto, Categoria, Tag, Pedido, DetallePedido, Pago, Slide, ConfiguracionSitio, SeccionCategoria, BannerFidelizacion, FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, ImagenProducto, ProyectoPortafolio, InstagramConfig, Descuento, Resena
from .services import FlowService, MercadoPagoService
from .instagram_service import InstagramService

def home(request):
    productos = Producto.objects.filter(activo=True).order_by('-fecha_creacion')[:8]
    categorias = Categoria.objects.filter(visible_navegacion=True)
    slides = Slide.objects.filter(activo=True)
    config = ConfiguracionSitio.objects.filter(activo=True).first()
    banners = BannerFidelizacion.objects.filter(activo=True)

    # Instagram
    instagram_config = InstagramConfig.objects.filter(activo=True, mostrar_en_home=True).first()
    instagram_posts = []
    if instagram_config:
        instagram_posts = InstagramService().get_user_media(instagram_config.cantidad_posts)

    secciones_categorias = SeccionCategoria.objects.filter(activo=True)
    secciones_con_productos = []
    for seccion in secciones_categorias:
        productos_seccion = Producto.objects.filter(categoria=seccion.categoria, activo=True)[:12]
        secciones_con_productos.append({'seccion': seccion, 'productos': productos_seccion})

    return render(request, 'home.html', {
        'productos': productos,
        'categorias': categorias,
        'slides': slides,
        'config': config,
        'banners': banners,
        'secciones_categorias': secciones_con_productos,
        'instagram_posts': instagram_posts,
        'instagram_config': instagram_config,
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
    atributos = producto.atributos.prefetch_related('valores').all()
    resenas = producto.resenas.filter(aprobada=True)
    promedio_resenas = resenas.aggregate(avg=models.Avg('puntuacion'))['avg']

    # Precio minimo para mostrar "Desde $X"
    precio_minimo = float(producto.precio)
    tiene_variantes = False
    for atributo in atributos:
        for v in atributo.valores.filter(activo=True):
            tiene_variantes = True
            precio_variante = float(producto.precio) + float(v.precio_extra)
            if precio_variante < precio_minimo:
                precio_minimo = precio_variante

    # Si hay opciones, el precio minimo es el menor precio de opcion
    opciones = list(producto.opciones.all())
    if opciones:
        precio_minimo_opcion = min(float(o.precio) for o in opciones)
        precio_minimo = precio_minimo_opcion

    # Serializar variantes para JS
    variantes_json = []
    for atributo in atributos:
        valores = []
        for v in atributo.valores.filter(activo=True):
            valores.append({
                'id': v.id,
                'valor': v.valor,
                'precio_extra': float(v.precio_extra),
                'stock': v.stock,
                'imagen': v.imagen_producto.imagen.url if v.imagen_producto and v.imagen_producto.imagen else None,
            })
        variantes_json.append({'nombre': atributo.nombre, 'valores': valores})

    # Opciones de precio
    opciones_json = []
    for op in opciones:
        opciones_json.append({
            'id': op.id,
            'nombre': op.nombre,
            'precio': float(op.precio),
        })

    return render(request, 'detalle_producto.html', {
        'producto': producto,
        'categorias': categorias,
        'config': config,
        'atributos': atributos,
        'variantes_json': json.dumps(variantes_json),
        'opciones_json': json.dumps(opciones_json),
        'precio_minimo': precio_minimo,
        'tiene_variantes': tiene_variantes,
        'resenas': resenas,
        'promedio_resenas': promedio_resenas,
        'total_resenas': resenas.count(),
    })

def carrito(request):
    return render(request, 'carrito.html')


@require_POST
def crear_resena(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    nombre = request.POST.get('nombre', '').strip()
    puntuacion = int(request.POST.get('puntuacion', 5))
    comentario = request.POST.get('comentario', '').strip()
    if nombre and comentario and 1 <= puntuacion <= 5:
        Resena.objects.create(
            producto=producto, nombre=nombre,
            puntuacion=puntuacion, comentario=comentario
        )
        messages.success(request, 'Tu reseña fue enviada y será publicada tras revisión.')
    else:
        messages.error(request, 'Por favor completa todos los campos.')
    return redirect('detalle_producto', producto_id=producto_id)

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
    # Decodificar caracteres especiales en la URL
    import urllib.parse
    tag_nombre = urllib.parse.unquote(tag_nombre)
    
    tag = get_object_or_404(Tag, nombre=tag_nombre, activo=True)
    
    # Buscar productos que tengan este tag tanto en tags_adicionales como en tags de categoría
    productos = Producto.objects.filter(
        activo=True
    ).filter(
        models.Q(tags_adicionales=tag) | models.Q(categoria__tags=tag)
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

@require_POST
def procesar_pago(request):
    try:
        # Verificar que el contenido sea JSON
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Content-Type debe ser application/json'}, status=400)
            
        data = json.loads(request.body)
        carrito = data.get('carrito', [])
        datos_envio = data.get('datosEnvio', {})
        metodo_pago = data.get('metodoPago')
        email = datos_envio.get('email', '')
        
        if not carrito:
            return JsonResponse({'error': 'Carrito vacío'}, status=400)
        if not metodo_pago:
            return JsonResponse({'error': 'Método de pago no seleccionado'}, status=400)
        if not email:
            return JsonResponse({'error': 'Email requerido'}, status=400)
        
        # Crear pedido
        total = sum(float(item['precio']) * int(item['cantidad']) for item in carrito)
        pedido = Pedido.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            total=total,
            estado='pendiente'
        )
        
        # Crear detalles del pedido y descontar stock
        for item in carrito:
            try:
                producto = Producto.objects.get(id=item['id'])
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=int(item['cantidad']),
                    precio=float(item['precio']),
                    personalizacion=item.get('personalizacion', '')
                )
                # Descontar stock general
                producto.stock = max(0, producto.stock - int(item['cantidad']))
                producto.save(update_fields=['stock'])
                # Descontar stock de variante si el nombre incluye variante
                nombre = item.get('personalizacion', '') or item.get('nombre', '')
                from .models import VarianteValor
                for valor in VarianteValor.objects.filter(
                    atributo__producto=producto, activo=True
                ):
                    if valor.valor in item.get('nombre', ''):
                        valor.stock = max(0, valor.stock - int(item['cantidad']))
                        valor.save(update_fields=['stock'])
            except Producto.DoesNotExist:
                return JsonResponse({'error': f'Producto {item["id"]} no encontrado'}, status=400)
        
        # Procesar pago según método
        try:
            if metodo_pago == 'flow':
                flow_service = FlowService()
                url_pago = flow_service.crear_pago(pedido, email)
                if url_pago:
                    return JsonResponse({'url': url_pago})
                else:
                    return JsonResponse({'error': 'Error al crear pago con Flow'}, status=500)
            elif metodo_pago == 'mercadopago':
                mp_service = MercadoPagoService()
                url_pago = mp_service.crear_pago(pedido, email)
                if url_pago:
                    return JsonResponse({'url': url_pago})
                else:
                    return JsonResponse({'error': 'Error al crear pago con MercadoPago'}, status=500)
            else:
                return JsonResponse({'error': 'Método de pago no válido'}, status=400)
        except Exception as payment_error:
            # Si Flow falla, sugerir MercadoPago
            if metodo_pago == 'flow':
                return JsonResponse({'error': 'Flow temporalmente no disponible. Por favor usa MercadoPago.'}, status=500)
            return JsonResponse({'error': f'Error en pasarela: {str(payment_error)}'}, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@csrf_exempt
@require_POST
def flow_confirmar(request):
    token = request.POST.get('token')
    
    if token:
        flow_service = FlowService()
        resultado = flow_service.verificar_pago(token)
        
        if resultado and resultado.get('status') == 2:  # Pagado
            try:
                pago = Pago.objects.get(token_pago=token)
                pago.estado = 'pagado'
                pago.fecha_pago = timezone.now()
                pago.datos_respuesta = resultado
                pago.save()
                
                pago.pedido.estado = 'procesando'
                pago.pedido.save()
                
                return HttpResponse('OK')
            except Pago.DoesNotExist:
                pass
    
    return HttpResponse('ERROR', status=400)

@csrf_exempt
@require_POST
def mercadopago_webhook(request):
    try:
        data = json.loads(request.body)
        
        if data.get('type') == 'payment':
            payment_id = data['data']['id']
            
            mp_service = MercadoPagoService()
            payment_info = mp_service.verificar_pago(payment_id)
            
            if payment_info and payment_info.get('status') == 'approved':
                external_reference = payment_info.get('external_reference')
                if external_reference:
                    pedido_id = external_reference.replace('ORD-', '')
                    try:
                        pedido = Pedido.objects.get(id=pedido_id)
                        pago, created = Pago.objects.get_or_create(
                            pedido=pedido,
                            defaults={
                                'metodo': 'mercadopago',
                                'monto': pedido.total,
                                'estado': 'pagado',
                                'fecha_pago': timezone.now(),
                                'id_transaccion': str(payment_id),
                                'datos_respuesta': payment_info
                            }
                        )
                        
                        if not created:
                            pago.estado = 'pagado'
                            pago.fecha_pago = timezone.now()
                            pago.datos_respuesta = payment_info
                            pago.save()
                        
                        pedido.estado = 'procesando'
                        pedido.save()
                        
                    except Pedido.DoesNotExist:
                        pass
        
        return HttpResponse('OK')
    except Exception as e:
        return HttpResponse('ERROR', status=400)

def pago_exitoso(request):
    return render(request, 'pago_exitoso.html')

def pago_fallido(request):
    return render(request, 'pago_fallido.html')

def pago_pendiente(request):
    return render(request, 'pago_pendiente.html')


def validar_cupon(request):
    codigo = request.GET.get('codigo', '').strip().upper()
    producto_id = request.GET.get('producto_id')
    if not codigo:
        return JsonResponse({'ok': False, 'error': 'Ingresa un código'})
    try:
        descuento = Descuento.objects.get(codigo__iexact=codigo)
        if not descuento.es_valido():
            return JsonResponse({'ok': False, 'error': 'Cupón no válido o expirado'})
        return JsonResponse({
            'ok': True,
            'tipo': descuento.tipo,
            'valor': float(descuento.valor),
            'aplica_a': descuento.aplica_a,
            'nombre': descuento.nombre,
            'productos_ids': list(descuento.productos.values_list('id', flat=True)),
            'categorias_ids': list(descuento.categorias.values_list('id', flat=True)),
        })
    except Descuento.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Cupón no encontrado'})


def portafolio(request):
    proyectos = ProyectoPortafolio.objects.filter(activo=True)
    categorias_usadas = proyectos.values_list('categoria', flat=True).distinct()
    categorias_disponibles = [
        (k, v) for k, v in ProyectoPortafolio.CATEGORIAS if k in categorias_usadas
    ]
    return render(request, 'portafolio.html', {
        'proyectos': proyectos,
        'categorias_disponibles': categorias_disponibles,
    })


@login_required
def configurador(request):
    if not request.user.is_staff:
        return redirect('home')
    config = ConfiguracionSitio.objects.filter(activo=True).first()
    footer = FooterConfig.objects.filter(activo=True).first()
    sobre_mi = SobreMi.objects.filter(activo=True).first()
    contacto = Contacto.objects.filter(activo=True).first()
    return render(request, 'configurador.html', {
        'config': config,
        'footer': footer,
        'sobre_mi': sobre_mi,
        'contacto': contacto,
    })


@login_required
def preview_home(request):
    """Vista del home sin X-Frame-Options para el iframe del configurador."""
    if not request.user.is_staff:
        return redirect('home')
    response = home(request)
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response


@login_required
@require_POST
def configurador_guardar(request):
    if not request.user.is_staff:
        return JsonResponse({'ok': False}, status=403)
    try:
        data = json.loads(request.body)
        seccion = data.get('seccion')

        if seccion == 'colores':
            config, _ = ConfiguracionSitio.objects.get_or_create(activo=True)
            for campo in ['color_primario', 'color_secundario', 'color_fondo', 'color_banner', 'color_cards', 'color_hover']:
                if campo in data:
                    setattr(config, campo, data[campo])
            if 'mensaje_envio' in data:
                config.mensaje_envio = data['mensaje_envio']
            config.save()

        elif seccion == 'footer':
            footer, _ = FooterConfig.objects.get_or_create(activo=True)
            for campo in ['color_fondo', 'color_texto', 'color_enlaces', 'color_hover', 'color_redes']:
                if campo in data:
                    setattr(footer, campo, data[campo])
            footer.save()

        elif seccion == 'sobre_mi':
            obj, _ = SobreMi.objects.get_or_create(activo=True)
            if 'titulo' in data: obj.titulo = data['titulo']
            if 'contenido' in data: obj.contenido = data['contenido']
            obj.save()

        elif seccion == 'contacto':
            obj, _ = Contacto.objects.get_or_create(activo=True)
            for campo in ['titulo', 'telefono', 'email', 'direccion', 'horarios']:
                if campo in data:
                    setattr(obj, campo, data[campo])
            obj.save()

        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)

@login_required
def debug_config(request):
    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    import os
    config = {
        'FLOW_API_KEY': bool(os.environ.get('FLOW_API_KEY', '')),
        'FLOW_SECRET_KEY': bool(os.environ.get('FLOW_SECRET_KEY', '')),
        'MERCADOPAGO_ACCESS_TOKEN': bool(os.environ.get('MERCADOPAGO_ACCESS_TOKEN', '')),
        'MERCADOPAGO_SANDBOX': os.environ.get('MERCADOPAGO_SANDBOX', 'Not set'),
        'SITE_URL': os.environ.get('SITE_URL', 'Not set'),
        'DEBUG': os.environ.get('DEBUG', 'Not set'),
        'RAILWAY_ENVIRONMENT': os.environ.get('RAILWAY_ENVIRONMENT', 'Not set')
    }
    return JsonResponse(config)

def obtener_imagen_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        img = producto.imagen_principal
        if not img:
            return JsonResponse({'imagen': None})
        return JsonResponse({'imagen': img.url})
    except Producto.DoesNotExist:
        return JsonResponse({'imagen': None})
    except Exception as e:
        import logging
        logging.error(f'Error obteniendo imagen: {str(e)}')
        return JsonResponse({'imagen': None})


def obtener_imagenes_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        imagenes = []
        for img in producto.imagenes.all():
            if img.imagen:
                imagenes.append({
                    'id': img.id,
                    'url': img.imagen.url,
                    'orden': img.orden,
                    'es_principal': img.es_principal,
                })
        return JsonResponse({'imagenes': imagenes})
    except Producto.DoesNotExist:
        return JsonResponse({'imagenes': []})


@login_required
def variantes_datos(request, producto_id):
    """Retorna datos de variantes guardados para poblar la tabla en el admin."""
    if not request.user.is_staff:
        return JsonResponse({}, status=403)
    from .models import VarianteAtributo
    try:
        producto = Producto.objects.get(id=producto_id)
        data = {}
        for atributo in producto.atributos.prefetch_related('valores__imagen_producto').all():
            valores_data = {}
            for v in atributo.valores.all():
                valores_data[v.valor] = {
                    'stock': v.stock,
                    'precio': float(v.precio),
                    'imagen_id': v.imagen_producto_id or '',
                    'imagen_url': v.imagen_producto.imagen.url if v.imagen_producto and v.imagen_producto.imagen else '',
                }
            data[atributo.nombre] = valores_data
        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({})

@csrf_exempt
@require_POST
def calcular_envio(request):
    try:
        data = json.loads(request.body)
        region = data.get('region')
        ciudad = data.get('ciudad')
        direccion = data.get('direccion')
        peso = data.get('peso', 1)
        
        # Token de Starken desde variables de entorno
        starken_token = os.environ.get('STARKEN_TOKEN')
        
        if not starken_token:
            return JsonResponse({
                'starken': 3500,  # Precio fijo si no hay token
                'bluexpress': 4200
            })
        
        # Calcular envío con Starken
        starken_precio = calcular_starken(region, ciudad, direccion, peso, starken_token)
        
        # BlueExpress (simulado por ahora)
        bluexpress_precio = int(starken_precio * 1.2) if starken_precio else 4200
        
        return JsonResponse({
            'starken': starken_precio,
            'bluexpress': bluexpress_precio
        })
        
    except Exception as e:
        return JsonResponse({
            'starken': 3500,  # Fallback
            'bluexpress': 4200
        })

def calcular_starken(region, ciudad, direccion, peso, token):
    try:
        # API de Starken para cotización
        url = 'https://api.starken.cl/v1/cotizacion'
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'origen': {
                'region': 'Metropolitana',
                'ciudad': 'Santiago',
                'direccion': 'Av. Providencia 1234'
            },
            'destino': {
                'region': region,
                'ciudad': ciudad,
                'direccion': direccion
            },
            'paquete': {
                'peso': peso,
                'largo': 30,
                'ancho': 20,
                'alto': 10
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('precio', 3500)
        else:
            return 3500  # Precio por defecto
            
    except Exception as e:
        return 3500  # Precio por defecto en caso de error

