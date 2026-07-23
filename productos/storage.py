from cloudinary_storage.storage import RawMediaCloudinaryStorage


class DigitalFileStorage(RawMediaCloudinaryStorage):
    """Almacena archivos digitales (PDF, ZIP) como raw autenticado en Cloudinary."""

    def _upload(self, name, content):
        import cloudinary.uploader
        options = {
            'use_filename': True,
            'unique_filename': True,
            'resource_type': 'raw',
            'type': 'authenticated',
        }
        return cloudinary.uploader.upload(content, **options)