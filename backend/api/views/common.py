from rest_framework import permissions, viewsets
from rest_framework_simplejwt import authentication

from backend.api.models import Event, ExternalLink
from backend.api.serializers.common import EventSerializer, ExternalLinkSerializer


class ExternalLinkViewSet(viewsets.ModelViewSet):
    queryset = ExternalLink.objects.all()
    serializer_class = ExternalLinkSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = [
        permissions.IsAdminUser | permissions.DjangoModelPermissionsOrAnonReadOnly
    ]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.order_by("start")
    serializer_class = EventSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = [
        permissions.IsAdminUser | permissions.DjangoModelPermissionsOrAnonReadOnly
    ]
    search_fields = ["name"]
