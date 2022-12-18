from rest_framework import serializers

from backend.api.models import Perk


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = ("text", "value", "tooltip")
