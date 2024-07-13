from rest_framework import serializers
import main.models


class TeamsSerializer(serializers.Serializer):

    def create(self, validated_data):
        return main.models.Team.object.create(**validated_data)

class GamesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(default='')
    date = serializers.DateTimeField(default = '1111-11-11 11:11')
    is_over = serializers.BooleanField(default=False)
    #questions = serializers.ModelField(main.models.Question)
    #teams = serializers.ManyRelatedField(main.models.Team)

    def create(self, validated_data):
        return main.models.Game.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)
        instance.is_over = validated_data.get("is_over", instance.is_over)
        #instance.questions = validated_data.get("questions", instance.questions)
        #instance.teams = validated_data.get("teams", instance.teams)
        instance.save()
        return instance


class NewsSerializer(serializers.Serializer):
    class Meta:
        model = main.models.News
        fields = '__all__'