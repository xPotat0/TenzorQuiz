from rest_framework import serializers
import main.models


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = main.models.Team
        fields = '__all__'

class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = main.models.Game
        fields = ('__all__')


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = main.models.Question
        fields = '__all__'


class NewsSerializer(serializers.Serializer):
    class Meta:
        model = main.models.News
        fields = '__all__'