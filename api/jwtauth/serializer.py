from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.core.utils import DotsValidationError


User = get_user_model()


class ReturnJWTTokensSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class BaseLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except Exception as e:
            raise DotsValidationError({"password": [str(e)]})

        self.user.last_login = timezone.now()
        self.user.updated_at = timezone.now()
        self.user.save(update_fields=["last_login", "updated_at"])

        user_roles = self.user.get_role_names()
        user_permissions = [p.codename for p in self.user.get_all_permissions_by_roles()]
        user_info = {
            "pk": self.user.id,
            "email": self.user.email,
            "full_name": self.user.name,
            "roles": user_roles,
            "permissions": user_permissions,
            "is_admin": self.user.is_admin,
            "is_regular_user": self.user.is_regular_user,
            "user_type": self.get_user_type()
        }

        data['user_info'] = user_info
        return data

    def get_user_type(self):
        if self.user.is_admin:
            return "admin"
        elif self.user.has_role('Manager'):
            return "manager"
        elif self.user.has_role('Moderator'):
            return "moderator"
        elif self.user.is_regular_user:
            return "user"
        else:
            return "unknown"



class AdminLoginSerializer(BaseLoginSerializer):
     def validate(self, attrs):
        validate_attrs = super().validate(attrs)
        if not self.user.is_admin:
            raise DotsValidationError({
                'admin': ["Invalid Admin credentials. Admin role required."]
            })
        
        return validate_attrs
