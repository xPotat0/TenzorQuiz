from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class User(models.Model):
    class Role(models.IntegerChoices):
        PLAYER = 0, _('Участник')
        MODERATOR = 1, _('Ведущий')

    class Gender(models.TextChoices):
        MALE = 'M', _('Мужчина')
        FEMALE = 'F', _('Женщина')
        UNDISCLOSED = 'U', _('-')

    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    password = models.CharField()
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.UNDISCLOSED,
        blank=True,
        null=True
    )
    description = models.TextField(blank=True, default='')
    role = models.IntegerField(choices=Role.choices, default=Role.PLAYER)
    access_token = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name

class LoginUser(models.Model):
     login = models.CharField(max_length=255)
     password = models.CharField(max_length=255)

     def __str__(self):
         return self.login

