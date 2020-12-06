from django.contrib.auth.models import User

from rest_framework import serializers

from .models import LibraryGame, BggGame, Withdraw, Player, Badge, Location


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'email')
        extra_kwargs = {
            'url': {'view_name': 'players', 'lookup_field': 'id'},
            'name': {'required': True},
            'email': {'required': True}
        }


class BggGameSerializer(serializers.ModelSerializer):
    badges = BadgeSerializer(many=True)

    class Meta:
        model = BggGame
        fields = (
            'bggid',
            'name',
            'rank',
            'thumbnail',
            'image',
            'min_playtime',
            'max_playtime',
            'min_players',
            'max_players',
            'badges'
        )


class WithdrawBaseSerializer(serializers.ModelSerializer):
    requisitor = PlayerSerializer(read_only=True)

    class Meta:
        model = Withdraw
        fields = ('id', 'requisitor')


class LibraryGameSerializer(serializers.ModelSerializer):
    game = BggGameSerializer(read_only=True)
    owner = PlayerSerializer(read_only=True)

    game_id = serializers.IntegerField(write_only=True, required=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all(), source="owner", required=True,
                                                  write_only=True)

    current_withdraw = WithdrawBaseSerializer(read_only=True)

    class Meta:
        model = LibraryGame
        fields = (
            'id',
            'game',
            'game_id',
            'owner',
            'owner_id',
            'notes',
            'location',
            'date_checkin',
            'date_checkout',
            'current_withdraw',
            'status',
        )


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'first_name', 'last_name')

    def get_name(self, data):
        return f"{data.first_name} {data.last_name}"


class WithdrawSerializer(serializers.ModelSerializer):
    game_id = serializers.PrimaryKeyRelatedField(queryset=LibraryGame.objects.all(),
                                                 source='game',
                                                 write_only=True,
                                                 required=True)
    requisitor_id = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all(),
                                                       source="requisitor",
                                                       required=True,
                                                       write_only=True)
    requisitor = PlayerSerializer(read_only=True)
    game = LibraryGameSerializer(read_only=True)

    class Meta:
        model = Withdraw
        fields = ('id', 'requisitor', 'requisitor_id', 'game', 'game_id', 'date_withdrawn', 'date_returned')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'