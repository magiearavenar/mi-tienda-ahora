from django.db import migrations, models
from django.utils.text import slugify
import unicodedata


def generar_slugs(apps, schema_editor):
    Producto = apps.get_model('productos', 'Producto')
    for p in Producto.objects.all():
        if not p.slug:
            base = slugify(unicodedata.normalize('NFKD', p.nombre))
            slug, n = base, 1
            while Producto.objects.filter(slug=slug).exclude(pk=p.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            p.slug = slug
            p.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0047_producto_archivo_digital_producto_es_digital_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, default=''),
        ),
        migrations.RunPython(generar_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='producto',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True),
        ),
    ]
