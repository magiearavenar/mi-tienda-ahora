from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0029_proyectoportafolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='productos/'),
        ),
        migrations.AlterField(
            model_name='imagenproducto',
            name='imagen',
            field=models.ImageField(max_length=500, upload_to='productos/'),
        ),
        migrations.AlterField(
            model_name='slide',
            name='imagen',
            field=models.ImageField(max_length=500, upload_to='slides/'),
        ),
    ]
