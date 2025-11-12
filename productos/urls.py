from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_categoria'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('buscar/', views.buscar, name='buscar'),
    path('tag/<str:tag_nombre>/', views.productos_por_tag, name='productos_tag'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Pagos
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
    path('flow/confirmar/', views.flow_confirmar, name='flow_confirmar'),
    path('mercadopago/webhook/', views.mercadopago_webhook, name='mercadopago_webhook'),
    path('pago/exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago/fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago/pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('debug/config/', views.debug_config, name='debug_config'),
    path('obtener-imagen/<int:producto_id>/', views.obtener_imagen_producto, name='obtener_imagen_producto'),
    path('calcular-envio/', views.calcular_envio, name='calcular_envio'),
]