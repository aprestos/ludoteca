from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import serializers

from backend.api.models import Event, ExternalLink


class ExternalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalLink
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class BulkCreateListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        """
        Bulk call of serializer.save.
        Useful when there is a list of objects provided in the same request (POST)
        :param validated_data:
        :return:
        """
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        return result
