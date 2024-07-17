from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueValidator

from teams.models import Team
from main.models import User


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='full_name')

    class Meta:
        model = User
        fields = ('username', )


class TeamsSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Team
        fields = ('team_id', 'team_name')


class TeamCreateSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='id', read_only=True)
    captain_id = serializers.IntegerField(required=True, validators=[UniqueValidator(
        queryset=Team.objects.all(), message='Команда с таким captain_id уже существует.')
    ])
    # team_name = serializers.CharField(source='name')
    # team_desc = serializers.CharField(source='description', required=False)

    class Meta:
        model = Team
        fields = ('team_id', 'captain_id', 'team_name', 'team_desc')

    def create(self, validated_data):
        captain_id = validated_data.get('captain_id')
        try:
            user = User.objects.get(pk=captain_id)
        except User.DoesNotExist:
            raise NotFound(detail=f'Пользователя с id {captain_id} не существует')
        team = Team.objects.create(**validated_data)
        team.team_members.add(user)
        team.save()
        return team


class TeamUpdateSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Team
        fields = ('team_id', 'team_name', 'team_desc')


class TeamSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='id', read_only=True)
    team_name = serializers.CharField()
    team_desc = serializers.CharField()
    team_points = serializers.FloatField(source='points')
    team_rating = serializers.IntegerField(source='rating')
    captain_name = serializers.CharField(source='get_captain_name', read_only=True)
    team_members = MemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ('team_id',
                  'team_name',
                  'team_desc',
                  'team_points',
                  'team_rating',
                  'captain_name', 'team_members')


class TeamListSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Team
        fields = ('team_id', 'team_name', 'creation_date', 'played_games', 'points', 'rating')


class TeamJoinSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    team_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Team
        fields = ('team_id', 'user_id')

    def validate_user_id(self, value):
        member = Team.objects.filter(team_members__id=value).first()
        if member is not None:
            raise serializers.ValidationError('Пользователь в таким user_id уже есть в команде')
        return value

    def add_member(self, user_id, team: Team):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound(detail=f'Пользователя с id {user_id} не существует')

        team.team_members.add(user)
        team.save()
        return team
