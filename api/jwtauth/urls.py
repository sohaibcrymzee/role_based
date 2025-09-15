from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.jwtauth import views

urlpatterns = [
    path("admin-login/", views.AdminLoginViewSet.as_view(), name="admin-login"),
]
