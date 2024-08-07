from rest_framework import serializers
from games.models import Game, Question, TeamQuestionAnswer
from teams.models import Team
from main.models import User


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'game_name', 'game_description', 'game_date', 'game_status']

class SingleGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class PlannedGameDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'game_name', 'game_description', 'game_status']

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_name', 'question_description', 'question_correct_answer', 'question_weight']

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
        model = Team
        fields = ['user_id']
