from django.contrib import admin
from .models import User, UserTeam
# Register your models here.

modelsToAdd = [User, UserTeam]

admin.site.register(modelsToAdd)