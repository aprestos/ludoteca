from abc import ABC
from typing import Type, TypeAlias

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from backend.api.models import Quota, Ticket
from backend.api.serializers.perk import PerkSerializer

User: TypeAlias = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class QuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = ("year", "user")


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    group_permissions = serializers.SerializerMethodField(read_only=True)
    groups = serializers.SerializerMethodField(read_only=True)
    # add_group = serializers.CharField(write_only=True)
    quotas = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ("password",)

    def get_name(self, data):
        return data.get_full_name()

    def get_group_permissions(self, obj: User):
        permissions = []
        for group in obj.groups.all():
            permissions.extend(group.permissions.all())

        return [p.codename for p in permissions]

    def get_quotas(self, obj: User):
        return [q.year for q in obj.quota_set.all()]

    def get_groups(self, obj: User):
        return [g.name for g in obj.groups.all()]

    # def create(self, validated_data):
    # group_data = validated_data.pop("add_group")
    # user = User.objects.create(**validated_data)

    # group = Group.objects.get(name=group_data)

    # user.groups.add(group)
    # return user


# Deprecated
class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "name", "email", "username")
        extra_kwargs = {
            "url": {"view_name": "players", "lookup_field": "id"},
            "first_name": {"required": True},
            "email": {"required": True},
            "username": {"required": True},
        }

    def get_name(self, obj: User):
        return obj.get_full_name()


class TicketSerializer(serializers.ModelSerializer):
    perks = PerkSerializer(many=True)

    class Meta:
        model = Ticket
        fields = "__all__"
