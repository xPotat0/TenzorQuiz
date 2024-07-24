from rest_framework import serializers
from django.contrib.auth import get_user_model
from games.serializers import GamesSerializer
from .models import News
from games.models import Game

User = get_user_model()


class NewsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(required=False, allow_null=True)
    games = GamesSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    news = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'news']


class GameForNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_name', 'game_description', 'game_date']
