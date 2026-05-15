# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0028_instagramconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProyectoPortafolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True)),
                ('categoria', models.CharField(choices=[('landing', 'Landing Page'), ('ecommerce', 'Tienda Online'), ('dashboard', 'Dashboard'), ('linktree', 'Linktree / Bio Link'), ('corporativo', 'Sitio Corporativo'), ('otro', 'Otro')], default='otro', max_length=20)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='portafolio/')),
                ('url_proyecto', models.URLField(blank=True, help_text='Link para ver el proyecto en vivo')),
                ('tecnologias', models.CharField(blank=True, help_text='Ej: Django, Bootstrap, PostgreSQL', max_length=200)),
                ('orden', models.IntegerField(default=0)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Proyecto',
                'verbose_name_plural': 'Portafolio Web',
                'ordering': ['orden', '-fecha_creacion'],
            },
        ),
    ]
