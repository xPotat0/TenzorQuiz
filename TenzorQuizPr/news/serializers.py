from rest_framework import serializers
from .models import News
from games.models import Game


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'image']


class GameForNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_name', 'game_description', 'game_date']
