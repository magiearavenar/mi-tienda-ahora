from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = 'miapp-media-magie'
    file_overwrite = False
    default_acl = 'public-read'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection.meta.client.meta.config.read_timeout = 300
        self.connection.meta.client.meta.config.connect_timeout = 60