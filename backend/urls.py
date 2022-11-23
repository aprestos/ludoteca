"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
from django.conf.urls import url
from django.contrib import admin
from django.http import FileResponse
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from backend.api.views import common, games, orders, statistics, users

router = routers.DefaultRouter()
router.register(r"library/games", games.LibraryGameViewSet)
router.register(r"library/withdraw", games.WithdrawViewSet)
router.register(r"library/locations", games.LocationViewSet)
router.register(r"store/suppliers", games.SupplierViewSet)
router.register(r"store/games", games.StoreGameViewSet)
router.register(r"users", users.UserViewSet)
router.register(r"players", users.PlayerViewSet)
router.register(r"quotas", users.QuotaViewSet)
router.register(r"events", common.EventViewSet)
router.register(r"tickets", users.TicketViewSet)
router.register(r"orders", orders.OrderViewSet)
router.register(r"products", orders.ProductViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))

urlpatterns = [
    path("", index_view, name="index"),
    path("auth/", include("rest_framework.urls")),
    # http://localhost:8000/api/admin/
    path("admin/", admin.site.urls),
    # http://localhost:8000/api/<router-viewsets>
    path("api/", include(router.urls)),
    # Authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/dashboard/", statistics.StatisticsViewSet.as_view(), name="dashboard"),
    path("settings/", include("settings.urls")),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("<path:path>", index_view),
]


# def index_view(request, path):
# return FileResponse(open("/public/index.html", "rb"))
