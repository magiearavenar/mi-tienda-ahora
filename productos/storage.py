from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = 'miapp-media-magie'
    file_overwrite = False
    default_acl = 'public-read'
    querystring_auth = False
    
    def _save(self, name, content):
        # Force public-read ACL on save
        self.object_parameters = {'ACL': 'public-read'}
        return super()._save(name, content)