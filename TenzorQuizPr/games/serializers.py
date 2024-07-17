from rest_framework import serializers
from games.models import Game, Question, TeamQuestionAnswer
from teams.models import Team
from main.models import User


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

class DeleteQuestionSerializer(serializers.ModelSerializer):
    ques_id = serializers.IntegerField()
    class Meta:
        model = Question
        fields =['ques_id']

class TeamQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamQuestionAnswer
        fields = '__all__'

class TeamToGameSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['user_id']
