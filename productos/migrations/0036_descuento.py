from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0035_variantevalor_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('tipo', models.CharField(choices=[('porcentaje', 'Porcentaje (%)'), ('monto', 'Monto fijo ($)')], default='porcentaje', max_length=20)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('aplica_a', models.CharField(choices=[('producto', 'Producto específico'), ('categoria', 'Categoría'), ('todos', 'Todos los productos')], default='todos', max_length=20)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('usos_maximos', models.IntegerField(blank=True, null=True)),
                ('usos_actuales', models.IntegerField(default=0)),
                ('productos', models.ManyToManyField(blank=True, to='productos.producto')),
                ('categorias', models.ManyToManyField(blank=True, to='productos.categoria')),
            ],
            options={'verbose_name': 'Descuento', 'verbose_name_plural': 'Descuentos', 'ordering': ['-activo', 'nombre']},
        ),
    ]
