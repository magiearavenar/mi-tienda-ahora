from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views_instagram import instagram_posts_api

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_categoria'),
    path('producto/<slug:slug>/', views.detalle_producto, name='detalle_producto'),
    path('producto/<int:pk>/', views.redirigir_producto_por_id, name='redirigir_producto_id'),
    path('producto/<slug:slug>/resena/', views.crear_resena, name='crear_resena'),
    path('carrito/', views.carrito, name='carrito'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('cambiar-contrasena/', auth_views.PasswordChangeView.as_view(
        template_name='cambiar_contrasena.html',
        success_url='/cambiar-contrasena/exito/'
    ), name='password_change'),
    path('cambiar-contrasena/exito/', auth_views.PasswordChangeDoneView.as_view(
        template_name='cambiar_contrasena_exito.html'
    ), name='password_change_done'),
    path('recuperar-contrasena/', auth_views.PasswordResetView.as_view(
        template_name='recuperar_contrasena.html',
        email_template_name='emails/recuperar_contrasena_email.html',
        success_url='/recuperar-contrasena/enviado/'
    ), name='password_reset'),
    path('recuperar-contrasena/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='recuperar_contrasena_enviado.html'
    ), name='password_reset_done'),
    path('recuperar-contrasena/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='recuperar_contrasena_confirmar.html',
        success_url='/recuperar-contrasena/completado/'
    ), name='password_reset_confirm'),
    path('recuperar-contrasena/completado/', auth_views.PasswordResetCompleteView.as_view(
        template_name='recuperar_contrasena_completado.html'
    ), name='password_reset_complete'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('buscar/', views.buscar, name='buscar'),
    path('tag/<str:tag_nombre>/', views.productos_por_tag, name='productos_tag'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Pagos
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
    path('flow/confirmar/', views.flow_confirmar, name='flow_confirmar'),
    path('mercadopago/webhook/', views.mercadopago_webhook, name='mercadopago_webhook'),
    path('pago/exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('descargar/<str:token>/', views.descargar_digital, name='descargar_digital'),
    path('pago/fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago/pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('validar-cupon/', views.validar_cupon, name='validar_cupon'),
    path('debug/config/', views.debug_config, name='debug_config'),
    path('obtener-imagen/<int:producto_id>/', views.obtener_imagen_producto, name='obtener_imagen_producto'),
    path('obtener-imagenes/<int:producto_id>/', views.obtener_imagenes_producto, name='obtener_imagenes_producto'),
    path('variantes-datos/<int:producto_id>/', views.variantes_datos, name='variantes_datos'),
    path('admin/busqueda-global/', views.admin_busqueda_global, name='admin_busqueda_global'),
    path('calcular-envio/', views.calcular_envio, name='calcular_envio'),
    path('verificar-digitales/', views.verificar_digitales, name='verificar_digitales'),
    path('api/instagram-posts/', instagram_posts_api, name='instagram_posts_api'),
    path('portafolio/', views.portafolio, name='portafolio'),
    path('configurador/', views.configurador, name='configurador'),
    path('configurador/guardar/', views.configurador_guardar, name='configurador_guardar'),
    path('configurador/preview/', views.preview_home, name='configurador_preview'),
]