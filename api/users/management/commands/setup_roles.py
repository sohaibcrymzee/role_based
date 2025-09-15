# management/commands/setup_roles.py
from django.core.management.base import BaseCommand
from django.db import transaction
from api.users.models import Role, Permission, RolePermission


class Command(BaseCommand):
    help = 'Setup initial roles and permissions'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.create_permissions()
            self.create_roles()
            self.assign_permissions_to_roles()
            self.stdout.write(
                self.style.SUCCESS('Successfully created roles and permissions')
            )

    def create_permissions(self):
        """Create all necessary permissions"""
        permissions_data = [
            # User Management
            ('view_users', 'View Users', 'Can view user list and details'),
            ('add_users', 'Add Users', 'Can create new users'),
            ('change_users', 'Change Users', 'Can edit user information'),
            ('delete_users', 'Delete Users', 'Can delete users'),
            
            # Role Management
            ('view_roles', 'View Roles', 'Can view roles and permissions'),
            ('add_roles', 'Add Roles', 'Can create new roles'),
            ('change_roles', 'Change Roles', 'Can edit roles and permissions'),
            ('delete_roles', 'Delete Roles', 'Can delete roles'),
            
            # Content Management (example)
            ('view_content', 'View Content', 'Can view content'),
            ('add_content', 'Add Content', 'Can create content'),
            ('change_content', 'Change Content', 'Can edit content'),
            ('delete_content', 'Delete Content', 'Can delete content'),
            ('publish_content', 'Publish Content', 'Can publish/unpublish content'),
            
            # System Settings
            ('view_settings', 'View Settings', 'Can view system settings'),
            ('change_settings', 'Change Settings', 'Can modify system settings'),
            
            # Reports
            ('view_reports', 'View Reports', 'Can view system reports'),
            ('export_data', 'Export Data', 'Can export system data'),
            
            # Profile Management
            ('view_profile', 'View Profile', 'Can view own profile'),
            ('change_profile', 'Change Profile', 'Can edit own profile'),
        ]

        created_permissions = []
        for codename, name, description in permissions_data:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                defaults={
                    'name': name,
                    'description': description
                }
            )
            if created:
                created_permissions.append(permission.name)

        if created_permissions:
            self.stdout.write(f'Created permissions: {", ".join(created_permissions)}')

    def create_roles(self):
        """Create basic roles"""
        roles_data = [
            ('Admin', 'Administrator with full system access'),
            ('User', 'Regular user with limited permissions'),
            ('Moderator', 'Content moderator with content management permissions'),
            ('Manager', 'Manager with user and content management permissions'),
        ]

        created_roles = []
        for name, description in roles_data:
            role, created = Role.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                created_roles.append(role.name)

        if created_roles:
            self.stdout.write(f'Created roles: {", ".join(created_roles)}')

    def assign_permissions_to_roles(self):
        """Assign permissions to roles"""
        
        # Admin gets all permissions
        admin_role = Role.objects.get(name='Admin')
        all_permissions = Permission.objects.all()
        for permission in all_permissions:
            RolePermission.objects.get_or_create(
                role=admin_role, 
                permission=permission
            )

        # User gets basic permissions
        user_role = Role.objects.get(name='User')
        user_permissions = [
            'view_profile',
            'change_profile',
            'view_content',
        ]
        for codename in user_permissions:
            try:
                permission = Permission.objects.get(codename=codename)
                RolePermission.objects.get_or_create(
                    role=user_role,
                    permission=permission
                )
            except Permission.DoesNotExist:
                continue

        # Moderator gets content management permissions
        moderator_role = Role.objects.get(name='Moderator')
        moderator_permissions = [
            'view_profile',
            'change_profile',
            'view_content',
            'add_content',
            'change_content',
            'delete_content',
            'publish_content',
            'view_users',
        ]
        for codename in moderator_permissions:
            try:
                permission = Permission.objects.get(codename=codename)
                RolePermission.objects.get_or_create(
                    role=moderator_role,
                    permission=permission
                )
            except Permission.DoesNotExist:
                continue

        # Manager gets user and content management permissions
        manager_role = Role.objects.get(name='Manager')
        manager_permissions = [
            'view_profile',
            'change_profile',
            'view_users',
            'add_users',
            'change_users',
            'view_content',
            'add_content',
            'change_content',
            'delete_content',
            'publish_content',
            'view_reports',
        ]
        for codename in manager_permissions:
            try:
                permission = Permission.objects.get(codename=codename)
                RolePermission.objects.get_or_create(
                    role=manager_role,
                    permission=permission
                )
            except Permission.DoesNotExist:
                continue

        self.stdout.write('Assigned permissions to roles')