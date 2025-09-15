from django.shortcuts import render

from api.jwtauth.serializer import AdminLoginSerializer, ProductSerializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenViewBase
from api.core.mixin import  DotsModelViewSet
from api.jwtauth.models import  Product
from api.core.permission import  HasRolePermission
# Create your views here.

class AdminLoginViewSet(TokenViewBase):
    serializer_class = AdminLoginSerializer
    permission_classes = [AllowAny]



class ProductViewSet(DotsModelViewSet):
    serializer_create_class =  ProductSerializers
    serializer_class = ProductSerializers
    queryset  = Product.objects.all()

    def get_permissions(self):
        permission_map = {
            "list": "product_view",
            "retrieve": "product_view",
            "create": "product_create",
            "update": "product_update",
            "partial_update": "product_update",
            "destroy": "product_delete",
        }
        permission_codename = permission_map.get(self.action)
        if permission_codename:
            return [IsAuthenticated, HasRolePermission(permission_codename)]
        return super().get_permissions()