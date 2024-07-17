from django.db import models
from teams.models import Team

class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    correct_answer = models.CharField(max_length=255)
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Game(models.Model):
    choices = ( ('active', 'active'),
                ('finished', 'finished'),
                ('planned', 'planned'))

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    date = models.DateTimeField()
    is_over = models.CharField(choices=choices, default='planned')
    questions = models.ManyToManyField(Question, blank=True)
    teams = models.ManyToManyField(Team, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name
    
class TeamQuestionAnswer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    score = models.FloatField(default=0.0, blank=True)
