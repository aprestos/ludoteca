from django.contrib.auth import get_user_model
from django.db.models import Count
from django_filters import rest_framework as django_filters
from rest_framework import filters, permissions, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt import authentication

from backend.api.filters import LibraryGameFilter, StoreGameFilter
from backend.api.models import LibraryGame, Location, StoreGame, Supplier, Withdraw
from backend.api.serializers.games import (
    AnonStoreGameSerializer,
    LibraryGameSerializer,
    LocationSerializer,
    StoreGameSerializer,
    SupplierSerializer,
    WithdrawSerializer,
)
from backend.api.utils import utils
from backend.api.utils.utils import StandardResultsSetPagination

User = get_user_model()


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.order_by("name")
    serializer_class = SupplierSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter, django_filters.DjangoFilterBackend)
    search_fields = ["name"]


class LibraryGameViewSet(viewsets.ModelViewSet):
    queryset = LibraryGame.objects.all().annotate(num_withdraws=Count("withdraw"))
    serializer_class = LibraryGameSerializer
    search_fields = ["game__name", "game__other_names"]
    filter_backends = (
        filters.SearchFilter,
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = LibraryGameFilter
    ordering_fields = [
        "game__name",
        "game__year",
        "game__rank",
        "game__weight",
        "num_withdraws",
    ]
    ordering = "game__name"
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    authentication_classes = [authentication.JWTAuthentication]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        bggid = serializer.initial_data["game_id"]
        game = utils.BGGGame.find(bggid)

        if game is None:
            game = utils.BGGGame.create(bggid)

        serializer.is_valid()
        serializer.save(game=game)


class StoreGameViewSet(viewsets.ModelViewSet):
    queryset = StoreGame.objects.all()
    search_fields = ["game__name", "game__other_names"]
    filter_backends = (
        filters.SearchFilter,
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )

    ordering_fields = ["game__name", "game__year", "game__rank", "selling_price"]
    ordering = "game__name"
    filterset_class = StoreGameFilter
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    authentication_classes = [authentication.JWTAuthentication]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StoreGameSerializer
        return AnonStoreGameSerializer

    def perform_create(self, serializer):
        bggid = serializer.initial_data["game_id"]
        game = utils.BGGGame.find(bggid)

        if game is None:
            game = utils.BGGGame.create(bggid)

        serializer.is_valid()
        serializer.save(game=game)


class WithdrawViewSet(viewsets.ModelViewSet):
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.order_by("name").all()
    serializer_class = LocationSerializer
