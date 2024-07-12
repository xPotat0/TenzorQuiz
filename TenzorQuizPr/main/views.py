from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
import main.models as models
import main.serializers as serializers

# Create your views here.
def index(request):
    return HttpResponse("<h4>Основная страница</h4>")

class TeamsViewSet(ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamsSerializer

class GamesViewSet(ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GamesSerializer

class NewsViewSet(ModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer
