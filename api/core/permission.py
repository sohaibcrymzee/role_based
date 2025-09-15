from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    message = {"permission": ["You don't have admin permissions"]}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.has_role('Admin')


class IsUser(permissions.BasePermission):
    message = {"permission": ["You don't have user permissions"]}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.has_role('User')


class IsModerator(permissions.BasePermission):
    message = {"permission": ["You don't have moderator permissions"]}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.has_role('Moderator')


class IsManager(permissions.BasePermission):
    message = {"permission": ["You don't have manager permissions"]}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.has_role('Manager')
