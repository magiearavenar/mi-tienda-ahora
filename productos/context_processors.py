from .models import FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, BannerFidelizacion, ConfiguracionSitio, Categoria, InstagramConfig
from collections import defaultdict

def footer_context(request):
    # Organizar categorías por categoría madre
    categorias_por_madre = defaultdict(list)
    categorias = Categoria.objects.filter(visible_navegacion=True)
    
    for categoria in categorias:
        if categoria.categoria_madre:
            categorias_por_madre[categoria.categoria_madre].append(categoria)
    
    return {
        'footer_config': FooterConfig.objects.filter(activo=True).first(),
        'sobre_mi': SobreMi.objects.filter(activo=True).first(),
        'contacto': Contacto.objects.filter(activo=True).first(),
        'informacion': Informacion.objects.filter(activo=True),
        'suscripcion': Suscripcion.objects.filter(activo=True).first(),
        'redes_sociales': RedSocial.objects.filter(activo=True),
        'banners': BannerFidelizacion.objects.filter(activo=True),
        'config': ConfiguracionSitio.objects.filter(activo=True).first(),
        'categorias': Categoria.objects.all(),
        'categorias_por_madre': dict(categorias_por_madre),
        'categorias_madre': Categoria.CATEGORIAS_MADRE,
        'instagram_config': InstagramConfig.objects.filter(activo=True, mostrar_en_home=True).first()
    }