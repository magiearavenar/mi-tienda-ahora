from .models import FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, BannerFidelizacion, ConfiguracionSitio, Categoria

def footer_context(request):
    return {
        'footer_config': FooterConfig.objects.filter(activo=True).first(),
        'sobre_mi': SobreMi.objects.filter(activo=True).first(),
        'contacto': Contacto.objects.filter(activo=True).first(),
        'informacion': Informacion.objects.filter(activo=True),
        'suscripcion': Suscripcion.objects.filter(activo=True).first(),
        'redes_sociales': RedSocial.objects.filter(activo=True),
        'banners': BannerFidelizacion.objects.filter(activo=True),
        'config': ConfiguracionSitio.objects.filter(activo=True).first(),
        'categorias': Categoria.objects.all()
    }