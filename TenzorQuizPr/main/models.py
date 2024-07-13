from django.db import models
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    creation_date = models.DateTimeField(auto_now_add=True)
    captain_id = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(default=0.0, blank=True)
    is_available = models.BooleanField(default=True)
    played_games_count = models.IntegerField(default=0, blank=True)
    members_count = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    correct_answer = models.CharField(max_length=255)
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    date = models.DateTimeField()
    is_over = models.BooleanField(default=False)
    questions = models.ManyToManyField(Question, blank=True)
    teams = models.ManyToManyField(Team, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    publication_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news/%Y-%m-%d/', blank=True)
    game = models.OneToOneField(Game, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title


class User(models.Model):
    class Role(models.IntegerChoices):
        PLAYER = 0, _('Участник'),
        MODERATOR = 1, _('Ведущий')

    full_name = models.CharField(max_length=100)
    gender = models.BooleanField(default=None, null=True)
    description = models.TextField(blank=True, default='')
    role = models.IntegerField(choices=Role.choices, default=Role.PLAYER)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class UserTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class TeamQuestionAnswer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    score = models.FloatField(default=0.0, blank=True)