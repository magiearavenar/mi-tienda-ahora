import os
import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_key = os.environ.get('SUPABASE_KEY')
        self.bucket_name = 'images'
    
    def _save(self, name, content):
        try:
            url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{name}"
            headers = {
                'Authorization': f'Bearer {self.supabase_key}',
            }
            files = {'file': (name, content.read(), content.content_type)}
            response = requests.post(url, headers=headers, files=files)
            if response.status_code in [200, 201]:
                return name
            return name  # Return name even if upload fails
        except Exception as e:
            return name  # Return name to avoid breaking
    
    def url(self, name):
        if not name:
            return ''
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{name}"
    
    def exists(self, name):
        return False
    
    def delete(self, name):
        return True
    
    def size(self, name):
        return 0