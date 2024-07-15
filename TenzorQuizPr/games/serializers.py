from rest_framework import serializers
from games.models import Game, Question, TeamQuestionAnswer


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'date']

class SingleGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class TeamQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamQuestionAnswer
        fields = ['team', 'question', 'is_correct']
