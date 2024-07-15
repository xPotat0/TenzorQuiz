from django.contrib import admin
from .models import Game, Question, TeamQuestionAnswer

# Register your models here.
admin.site.register(Game)
admin.site.register(Question)
admin.site.register(TeamQuestionAnswer)