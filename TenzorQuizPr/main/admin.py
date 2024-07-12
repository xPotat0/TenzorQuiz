from django.contrib import admin
from .models import Team, Game, News, User, Question, TeamQuestionAnswer
# Register your models here.

modelsToAdd = [Team, Game, News, User, Question, TeamQuestionAnswer]

admin.site.register(modelsToAdd)