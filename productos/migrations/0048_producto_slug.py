from django.db import migrations, models
from django.utils.text import slugify
import unicodedata


def agregar_columna_y_slugs(apps, schema_editor):
    # Agregar columna si no existe
    schema_editor.execute("""
        ALTER TABLE productos_producto
        ADD COLUMN IF NOT EXISTS slug varchar(250) NOT NULL DEFAULT '';
    """)
    # Generar slugs
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
    # Agregar unique constraint si no existe
    schema_editor.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'productos_producto_slug_key'
            ) THEN
                ALTER TABLE productos_producto ADD CONSTRAINT productos_producto_slug_key UNIQUE (slug);
            END IF;
        END $$;
    """)
    # Agregar índice LIKE si no existe
    schema_editor.execute("""
        CREATE INDEX IF NOT EXISTS productos_producto_slug_8e5f75e2_like
        ON productos_producto (slug varchar_pattern_ops);
    """)


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0047_producto_archivo_digital_producto_es_digital_and_more'),
    ]

    operations = [
        migrations.RunPython(agregar_columna_y_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='producto',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True),
        ),
    ]
