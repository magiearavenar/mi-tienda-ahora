from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0031_categoria_categoria_madre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='categoria',
        ),
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.ManyToManyField(
                blank=True,
                to='productos.Categoria',
                verbose_name='Categorías'
            ),
        ),
    ]
