from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0030_alter_imagen_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='categoria_madre',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='subcategorias',
                to='productos.categoria',
                help_text='Si esta es una subcategoría, selecciona la categoría principal'
            ),
        ),
    ]
