import requests
from django.conf import settings

class InstagramService:
    def __init__(self):
        self.access_token = getattr(settings, 'INSTAGRAM_ACCESS_TOKEN', None)
        self.base_url = 'https://graph.instagram.com/v21.0'

    def get_user_media(self, limit=6):
        if not self.access_token:
            return []
        try:
            # Obtener ID del usuario
            me = requests.get(
                f'{self.base_url}/me',
                params={'fields': 'user_id', 'access_token': self.access_token},
                timeout=3
            ).json()
            user_id = me.get('user_id') or me.get('id')
            if not user_id:
                return []

            # Obtener media
            resp = requests.get(
                f'{self.base_url}/{user_id}/media',
                params={
                    'fields': 'id,media_type,media_url,thumbnail_url,permalink,caption,timestamp',
                    'limit': limit,
                    'access_token': self.access_token
                },
                timeout=3
            )
            if resp.status_code == 200:
                return self._format(resp.json().get('data', []))
            return []
        except Exception as e:
            print(f'Instagram error: {e}')
            return []

    def _format(self, posts):
        result = []
        for p in posts:
            if p.get('media_type') == 'VIDEO':
                img = p.get('thumbnail_url')
            else:
                img = p.get('media_url')
            if not img:
                continue
            caption = p.get('caption', '') or ''
            result.append({
                'id': p['id'],
                'image_url': img,
                'permalink': p.get('permalink', 'https://instagram.com'),
                'caption': caption[:100] + ('...' if len(caption) > 100 else ''),
                'media_type': p.get('media_type', 'IMAGE'),
            })
        return result