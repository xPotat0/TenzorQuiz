from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Добавляем роль пользователя в токен
        token['role'] = user.role
        return token