from cloudinary_storage.storage import RawMediaCloudinaryStorage
import cloudinary.uploader


class DigitalFileStorage(RawMediaCloudinaryStorage):
    """Almacena archivos digitales (PDF, ZIP) como raw público en Cloudinary."""

    def _upload(self, name, content):
        return cloudinary.uploader.upload(
            content,
            resource_type='raw',
            type='upload',
            access_mode='public',
            use_filename=True,
            unique_filename=True,
        )