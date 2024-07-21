from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import News

User = get_user_model()


class NewsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = News
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    news = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'news']
