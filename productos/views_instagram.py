from django.http import JsonResponse
from .models import InstagramConfig
from .instagram_service import InstagramService

def instagram_posts_api(request):
    """API endpoint para obtener posts de Instagram"""
    config = InstagramConfig.objects.filter(activo=True).first()
    
    if not config:
        return JsonResponse({'posts': []})
    
    service = InstagramService()
    posts = service.get_user_media(config.cantidad_posts)
    
    return JsonResponse({
        'posts': posts,
        'username': config.usuario
    })