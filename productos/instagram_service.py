import requests
import json
from django.conf import settings

class InstagramService:
    def __init__(self):
        # Token de acceso de Instagram Basic Display API
        self.access_token = getattr(settings, 'INSTAGRAM_ACCESS_TOKEN', None)
        self.base_url = 'https://graph.instagram.com'
    
    def get_user_media(self, limit=6):
        """Obtiene los posts recientes del usuario"""
        if not self.access_token:
            return self._get_placeholder_posts(limit)
        
        try:
            url = f"{self.base_url}/me/media"
            params = {
                'fields': 'id,media_type,media_url,thumbnail_url,permalink,caption',
                'limit': limit,
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_posts(data.get('data', []))
            else:
                return self._get_placeholder_posts(limit)
                
        except Exception as e:
            print(f"Error al obtener posts de Instagram: {e}")
            return self._get_placeholder_posts(limit)
    
    def _format_posts(self, posts):
        """Formatea los posts de Instagram"""
        formatted_posts = []
        for post in posts:
            # Usar thumbnail para videos, media_url para imágenes
            image_url = post.get('thumbnail_url') or post.get('media_url')
            
            formatted_posts.append({
                'id': post.get('id'),
                'image_url': image_url,
                'permalink': post.get('permalink'),
                'caption': post.get('caption', '')[:100] + '...' if post.get('caption') else ''
            })
        
        return formatted_posts
    
    def _get_placeholder_posts(self, limit):
        """Posts placeholder cuando no hay API configurada"""
        posts = []
        for i in range(1, limit + 1):
            posts.append({
                'id': f'placeholder_{i}',
                'image_url': f'https://picsum.photos/300/300?random={i}',
                'permalink': 'https://instagram.com/mundomagie.cl',
                'caption': f'Post de ejemplo {i}'
            })
        return posts