from functools import wraps
from rest_framework.exceptions import PermissionDenied


def check_permission(user, permission_codename, method=None):
    """
    Check if a user has the given permission via roles.

    :param user: User instance
    :param permission_codename: str - permission codename to check
    :param method: Optional[str] - HTTP method (GET, POST, PUT, DELETE, etc.)
    :return: bool
    """

    try:
        # Must be active
        if not user.is_authenticated or not user.is_active:
            return False

        # Superuser bypass
        # if user.is_superuser:
        #     return True

        # Method-based filtering (optional, extendable)
        if method and method.upper() not in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return False

        # Role-based permission check
        return user.has_permission_by_role(permission_codename)
    except Exception as e:
        # Log errors if needed
        print(f"Permission check failed: {e}")
        return False


class HasRolePermission(BasePermission):
    """
    Custom DRF permission that checks role-based permissions.
    """

    def __init__(self, permission_codename, method=None):
        self.permission_codename = permission_codename
        self.method = method

    def has_permission(self, request, view):
        return check_permission(
            user=request.user,
            permission_codename=self.permission_codename,
            method=request.method
        )