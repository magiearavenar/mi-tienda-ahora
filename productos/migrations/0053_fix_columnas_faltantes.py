from django.db import migrations


SQL_COLUMNS = [
    ("productos_contacto",          "whatsapp",              "VARCHAR(20) NOT NULL DEFAULT ''"),
    ("productos_contacto",          "whatsapp_mensaje",      "VARCHAR(200) NOT NULL DEFAULT 'Hola! Me interesa un producto'"),
    ("productos_configuracionsitio","moneda_simbolo",        "VARCHAR(5) NOT NULL DEFAULT '$'"),
    ("productos_configuracionsitio","seo_descripcion",       "VARCHAR(160) NOT NULL DEFAULT ''"),
    ("productos_configuracionsitio","seo_titulo",            "VARCHAR(70) NOT NULL DEFAULT ''"),
]


def forwards(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        for table, col, definition in SQL_COLUMNS:
            cursor.execute("""
                SELECT 1 FROM information_schema.columns
                WHERE table_name = %s AND column_name = %s
            """, [table, col])
            if not cursor.fetchone():
                cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN "{col}" {definition}')


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0052_configuracion_seo_moneda'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
