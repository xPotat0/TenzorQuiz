from django.contrib import admin
from .models import User
# Register your models here.

modelsToAdd = [User]

admin.site.register(modelsToAdd)

