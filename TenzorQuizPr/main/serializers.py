from rest_framework.serializers import ModelSerializer
import main.models


class TeamsSerializer(ModelSerializer):
    class Meta:
        model = main.models.Team
        fields = '__all__'

class GamesSerializer(ModelSerializer):
    class Meta:
        model = main.models.Game
        fields = '__all__'

class NewsSerializer(ModelSerializer):
    class Meta:
        model = main.models.News
        fields = '__all__'