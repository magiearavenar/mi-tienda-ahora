from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0036_descuento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variantevalor',
            name='imagen',
        ),
        migrations.AddField(
            model_name='variantevalor',
            name='imagen_producto',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='variantes',
                to='productos.imagenproducto',
                help_text='Imagen del producto que se muestra al elegir esta variante'
            ),
        ),
    ]
