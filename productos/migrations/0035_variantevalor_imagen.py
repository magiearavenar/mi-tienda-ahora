from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0034_varianteatributo_valores_texto'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantevalor',
            name='imagen',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='variantes/'),
        ),
    ]
