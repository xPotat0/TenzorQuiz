from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .models import User, Role


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return {'tokens': data,
                'user': self.user}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'gender', 'description']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    role = serializers.ChoiceField(choices=Role.choices, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'email', 'password', 'gender']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
