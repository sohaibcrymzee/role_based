from django.urls import include, path
from rest_framework.routers import DefaultRouter



router = DefaultRouter(trailing_slash=False)


urlpatterns = router.urls + [
    path("auth/", include("api.jwtauth.urls")),
]
