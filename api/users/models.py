from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from api.core.models import (
    CharFieldSizes,
    BaseModel,
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The username field required")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)



class Permission(BaseModel):
    """
    Custom permission model for fine-grained access control
    """
    name = models.CharField(max_length=CharFieldSizes.MEDIUM, unique=True)
    codename = models.CharField(max_length=CharFieldSizes.MEDIUM, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = "permissions"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Role(BaseModel):
    """
    Role model that groups permissions together
    """
    name = models.CharField(max_length=CharFieldSizes.MEDIUM, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(
        Permission, 
        through='RolePermission',
        related_name='roles',
        blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "roles"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def add_permission(self, permission):
        """Add a permission to this role"""
        RolePermission.objects.get_or_create(role=self, permission=permission)

    def remove_permission(self, permission):
        """Remove a permission from this role"""
        RolePermission.objects.filter(role=self, permission=permission).delete()

    def has_permission(self, permission_codename):
        """Check if this role has a specific permission"""
        return self.permissions.filter(codename=permission_codename).exists()


class RolePermission(BaseModel):
    """
    Through model for Role-Permission many-to-many relationship
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = "role_permissions"
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


class UserRole(models.Model):
    """
    Through model for User-Role many-to-many relationship
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    class Meta:
        db_table = "user_roles"
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"

class User(AbstractUser, PermissionsMixin):
    name = models.CharField(max_length=CharFieldSizes.MEDIUM, default='Hello User')
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, null=True)
    first_name = None
    last_name = None
    username = None
    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    roles = models.ManyToManyField(
        Role, 
        through=UserRole,
        related_name='users',
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ["id"]
        db_table = "users"

    def __str__(self):
        return self.email
    
    def assign_role(self, role, assigned_by=None):
        """Assign a role to this user"""
        user_role, created = UserRole.objects.get_or_create(
            user=self, 
            role=role,
        )
        return user_role

    def remove_role(self, role):
        """Remove a role from this user"""
        UserRole.objects.filter(user=self, role=role).delete()

    def has_role(self, role_name):
        """Check if user has a specific role"""
        return self.roles.filter(name=role_name).exists()

    def has_permission_by_role(self, permission_codename):
        """Check if user has a specific permission through their roles"""
        return Permission.objects.filter(
            roles__users=self,
            codename=permission_codename
        ).exists()

    def get_all_permissions_by_roles(self):
        """Get all permissions for this user through their roles"""
        return Permission.objects.filter(roles__users=self).distinct()

    def get_role_names(self):
        """Get list of role names for this user"""
        return list(self.roles.values_list('name', flat=True))
    
    @property
    def is_admin(self):
        """Check if user has admin role"""
        return self.has_role('Admin')

    @property
    def is_regular_user(self):
        """Check if user has user role"""
        return self.has_role('User')





