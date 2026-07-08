from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0048_producto_slug'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE productos_detallepedido ADD COLUMN IF NOT EXISTS imagen_personalizacion varchar(100) NULL;",
            reverse_sql="ALTER TABLE productos_detallepedido DROP COLUMN IF EXISTS imagen_personalizacion;",
        ),
    ]
