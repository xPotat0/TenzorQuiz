from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Game)
admin.site.register(Question)
admin.site.register(News)
admin.site.register(Team)
admin.site.register(User)
admin.site.register(TeamQuestionAnswer)
