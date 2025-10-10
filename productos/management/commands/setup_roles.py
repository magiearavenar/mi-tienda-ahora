from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from productos.models import Producto, Categoria, Pedido

class Command(BaseCommand):
    help = 'Configura roles y permisos'

    def handle(self, *args, **options):
        # Crear grupos
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        cliente_group, created = Group.objects.get_or_create(name='Clientes')
        
        # Permisos para administradores
        admin_permissions = Permission.objects.filter(
            content_type__in=ContentType.objects.filter(
                model__in=['producto', 'categoria', 'pedido', 'detallepedido']
            )
        )
        admin_group.permissions.set(admin_permissions)
        
        # Configurar usuario margarett como admin
        try:
            margarett = User.objects.get(username='margarett')
            margarett.is_staff = True
            margarett.is_superuser = True
            margarett.groups.clear()
            margarett.groups.add(admin_group)
            margarett.save()
            self.stdout.write(f'Usuario margarett configurado como administrador')
        except User.DoesNotExist:
            self.stdout.write('Usuario margarett no existe')
        
        # Crear usuario cliente de ejemplo
        cliente, created = User.objects.get_or_create(
            username='cliente1',
            defaults={
                'email': 'cliente1@ejemplo.com',
                'is_staff': False,
                'is_superuser': False
            }
        )
        if created:
            cliente.set_password('cliente123')
            cliente.save()
        
        cliente.groups.clear()
        cliente.groups.add(cliente_group)
        
        self.stdout.write(f'Roles configurados correctamente')
        self.stdout.write(f'Usuario cliente1 creado con contraseña: cliente123')