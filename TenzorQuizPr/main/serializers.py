import jwt
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

import settings
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


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        # data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
            if settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    raise Exception
            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

        decoded_payload = jwt.decode(str(refresh),
                                     settings.SIMPLE_JWT['SIGNING_KEY'],
                                     algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        user_uid = decoded_payload['id']
        user = User.objects.filter(id=user_uid).first()
        refresh.payload.update({'role': user.role})
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user
        }


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
