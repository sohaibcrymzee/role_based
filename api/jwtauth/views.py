from django.shortcuts import render

from api.jwtauth.serializer import AdminLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenViewBase
# Create your views here.

class AdminLoginViewSet(TokenViewBase):
    serializer_class = AdminLoginSerializer
    permission_classes = [AllowAny]