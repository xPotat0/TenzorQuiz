from rest_framework import serializers
from teams.models import Team


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
