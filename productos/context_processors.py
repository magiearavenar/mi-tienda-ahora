from .models import FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, BannerFidelizacion, ConfiguracionSitio, Categoria, InstagramConfig

def footer_context(request):
    # Categorias madre con sus subcategorias precargadas
    categorias_madre = Categoria.objects.filter(
        categoria_madre__isnull=True,
        visible_navegacion=True
    ).prefetch_related('subcategorias')

    return {
        'footer_config': FooterConfig.objects.filter(activo=True).first(),
        'sobre_mi': SobreMi.objects.filter(activo=True).first(),
        'contacto': Contacto.objects.filter(activo=True).first(),
        'informacion': Informacion.objects.filter(activo=True),
        'suscripcion': Suscripcion.objects.filter(activo=True).first(),
        'redes_sociales': RedSocial.objects.filter(activo=True),
        'banners': BannerFidelizacion.objects.filter(activo=True),
        'config': ConfiguracionSitio.objects.filter(activo=True).first(),
        'categorias': Categoria.objects.filter(visible_navegacion=True),
        'categorias_madre': categorias_madre,
        'instagram_config': InstagramConfig.objects.filter(activo=True, mostrar_en_home=True).first()
    }