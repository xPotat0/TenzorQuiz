import jwt
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

import settings
from .models import User, Role
from teams.serializers import TeamsSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    user_name = serializers.CharField(source='username', read_only=True)
    user_email = serializers.CharField(source='email', read_only=True)
    user_role = serializers.SerializerMethodField()
    user_gender = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('user_id', 'user_name', 'user_email', 'user_role', 'user_gender')

    def get_user_teams(self, obj):
        user_teams = User.objects.get(id=obj.id).teams.all()
        is_captain = False
        for team in user_teams:
            if obj.id == team.captain_id:
                is_captain = True
        user_team_data = TeamsSerializer(user_teams, many=True).data
        return user_team_data, is_captain

    def get_user_role(self, obj):
        if obj.role == 'player':
            return "Участник"
        return "Ведущий"

    def get_user_gender(self, obj):
        if obj.gender == 'male':
            return "Мужчина"
        return "Женщина"


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='username', required=False)
    user_gender = serializers.CharField(source='gender', required=False)

    class Meta:
        model = User
        fields = ('user_name', 'user_gender')


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
