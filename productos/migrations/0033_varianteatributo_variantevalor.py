from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0032_producto_categoria_m2m'),
    ]

    operations = [
        migrations.CreateModel(
            name='VarianteAtributo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ej: Talla, Color, Material', max_length=100)),
                ('orden', models.IntegerField(default=0)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atributos', to='productos.producto')),
            ],
            options={'ordering': ['orden'], 'verbose_name': 'Atributo de variante', 'verbose_name_plural': 'Atributos de variantes'},
        ),
        migrations.CreateModel(
            name='VarianteValor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(help_text='Ej: S, Rojo, 200 hojas', max_length=100)),
                ('precio_extra', models.DecimalField(decimal_places=2, default=0, help_text='Precio adicional sobre el precio base', max_digits=10)),
                ('stock', models.IntegerField(default=0)),
                ('activo', models.BooleanField(default=True)),
                ('orden', models.IntegerField(default=0)),
                ('atributo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valores', to='productos.varianteatributo')),
            ],
            options={'ordering': ['orden'], 'verbose_name': 'Valor de variante', 'verbose_name_plural': 'Valores de variantes'},
        ),
    ]
