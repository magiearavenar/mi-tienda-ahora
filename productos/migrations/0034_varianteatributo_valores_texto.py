from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0033_varianteatributo_variantevalor'),
    ]

    operations = [
        migrations.AddField(
            model_name='varianteatributo',
            name='valores_texto',
            field=models.CharField(
                blank=True,
                help_text='Escribe los valores separados por coma. Ej: S, M, L, XL',
                max_length=500,
            ),
        ),
    ]
