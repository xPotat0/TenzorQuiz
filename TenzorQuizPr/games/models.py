from django.db import models
from teams.models import Team
from main.models import User

class Question(models.Model):
    question_name = models.CharField(max_length=100)
    question_description = models.TextField()
    question_correct_answer = models.CharField(max_length=255)
    question_weight = models.FloatField(default=0.0)

    def __str__(self):
        return self.question_name
    
    class Meta:
        ordering = ['question_name']

class Game(models.Model):
    choices = ( ('active', 'active'),
                ('finished', 'finished'),
                ('planned', 'planned'))

    game_name = models.CharField(max_length=100)
    game_description = models.TextField(blank=True, default='')
    game_date = models.DateTimeField()
    game_status = models.CharField(choices=choices, default='planned')
    game_questions = models.ManyToManyField(Question, blank=True)
    game_teams = models.ManyToManyField(Team, blank=True)
    game_creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-game_date']

    def __str__(self):
        return self.game_name
    
class TeamQuestionAnswer(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)#Не даёт достать вопросы, если название answer_game
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_team_answer = models.CharField()
    answer_is_correct = models.BooleanField(default=False)
    answer_score = models.FloatField(default=0.0, blank=True)
