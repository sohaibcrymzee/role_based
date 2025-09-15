from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.jwtauth.views import ProductViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"product", ProductViewSet, basename="products")
urlpatterns = router.urls + [
    path("auth/", include("api.jwtauth.urls")),
]
