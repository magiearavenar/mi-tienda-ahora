from django.db import migrations, models


def limpiar_tokens_duplicados(apps, schema_editor):
    """Elimina tokens duplicados (mismo producto+pedido+usado=False), conserva el más reciente."""
    TokenDescarga = apps.get_model('productos', 'TokenDescarga')
    from django.db.models import Max

    # Encontrar combinaciones duplicadas con usado=False
    vistos = {}
    for token in TokenDescarga.objects.filter(usado=False).order_by('-id'):
        clave = (token.producto_id, token.pedido_id)
        if clave in vistos:
            # Eliminar el duplicado más antiguo
            token.delete()
        else:
            vistos[clave] = token.id


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0055_config_color_nav'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokendescarga',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='tokendescarga',
            name='email_destino',
            field=models.EmailField(blank=True, default=''),
        ),
        migrations.RunPython(limpiar_tokens_duplicados, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='tokendescarga',
            constraint=models.UniqueConstraint(
                condition=models.Q(usado=False),
                fields=['producto', 'pedido'],
                name='unique_token_activo_por_producto_pedido',
            ),
        ),
    ]
