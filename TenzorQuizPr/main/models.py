from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

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


class LoginUser(models.Model):
     login = models.CharField(max_length=255)
     password = models.CharField(max_length=255)

     def __str__(self):
         return self.login