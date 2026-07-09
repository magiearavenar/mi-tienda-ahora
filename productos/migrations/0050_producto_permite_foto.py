from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0049_detallepedido_imagen_personalizacion'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE productos_producto ADD COLUMN IF NOT EXISTS permite_foto boolean NOT NULL DEFAULT false;
                ALTER TABLE productos_producto ADD COLUMN IF NOT EXISTS texto_foto varchar(200) NOT NULL DEFAULT 'Sube tu foto de referencia';
                ALTER TABLE productos_producto ADD COLUMN IF NOT EXISTS placeholder_foto varchar(200) NOT NULL DEFAULT 'Ej: foto de tu mascota, logo, diseño...';
            """,
            reverse_sql="""
                ALTER TABLE productos_producto DROP COLUMN IF EXISTS permite_foto;
                ALTER TABLE productos_producto DROP COLUMN IF EXISTS texto_foto;
                ALTER TABLE productos_producto DROP COLUMN IF EXISTS placeholder_foto;
            """,
        ),
    ]
