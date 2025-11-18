from .models import FooterConfig, SobreMi, Contacto, Informacion, Suscripcion, RedSocial, BannerFidelizacion, ConfiguracionSitio, Categoria, InstagramConfig

def footer_context(request):
    try:
        # Organizar categorías por categoría madre
        categorias_por_madre = {}
        categorias = Categoria.objects.filter(visible_navegacion=True)
        
        for categoria in categorias:
            if hasattr(categoria, 'categoria_madre') and categoria.categoria_madre:
                if categoria.categoria_madre not in categorias_por_madre:
                    categorias_por_madre[categoria.categoria_madre] = []
                categorias_por_madre[categoria.categoria_madre].append(categoria)
        
        categorias_madre = [
            ('PAPELERIA', 'PAPELERÍA'),
            ('COTILLON', 'COTILLÓN'),
            ('ACCESORIOS', 'ACCESORIOS'),
            ('NAVIDAD', 'NAVIDAD'),
            ('ESTAMPADOS', 'ESTAMPADOS'),
        ]
        
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
            'categorias_por_madre': categorias_por_madre,
            'categorias_madre': categorias_madre,
        }
    except Exception as e:
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
            'categorias_por_madre': {},
            'categorias_madre': [],
        }