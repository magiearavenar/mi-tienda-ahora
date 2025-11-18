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
import json
import requests
import os
from .models import Producto, Categoria, Tag, Pedido, DetallePedido, Pago, Slide, ConfiguracionSitio, SeccionCategoria, BannerFidelizacion, FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, ImagenProducto
from .services import FlowService, MercadoPagoService

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

@csrf_exempt
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
        
        # Crear detalles del pedido
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

def debug_config(request):
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
        imagen_principal = producto.imagen_principal()
        
        if not imagen_principal:
            return JsonResponse({'imagen': None})
        
        return JsonResponse({'imagen': imagen_principal.url})
            
    except Producto.DoesNotExist:
        return JsonResponse({'imagen': None})
    except Exception as e:
        import logging
        logging.error(f'Error obteniendo imagen: {str(e)}')
        return JsonResponse({'imagen': None})

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

