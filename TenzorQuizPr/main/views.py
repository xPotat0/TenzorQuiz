from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
import main.models as models
import main.serializers as serializers

# Create your views here.
def index(request):
    return HttpResponse("<h4>Основная страница</h4>")

class TeamsAPIView(APIView):
    def getAll():
        return Response({'Status': 'Accepted', 'Content': list(models.Team.objects.all().values())})

    def get(self, request):
        if True:
            response = TeamsAPIView.getAll()
        return response


class GamesAPIView(APIView):
    def get(self, requset, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            try:
                instance = models.Game.objects.get(pk=pk)
            except:
                return Response({'error': 'Object not found'})
            
            return Response({'Status': 'Accepted', 'Content': serializers.GamesSerializer(instance).data})

        games = models.Game.objects.all()
        content = serializers.GamesSerializer(games, many=True).data
        for game in content:
            ques_list = []
            team_list = []
            for ques in game["questions"]:
                ques_cont = serializers.QuestionsSerializer(models.Question.objects.get(pk=ques))
                ques_list.append(ques_cont.data)
            for team in game["teams"]:
                team_cont = serializers.TeamsSerializer(models.Team.objects.get(pk=team))
                team_list.append(team_cont.data)
            game['questions'] = ques_list
            game['teams'] = team_list
        return Response({'Status': 'Accepted', 'Content': content})
    

    def post(self, request):
        serializer = serializers.GamesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'New object created': serializer.data})



    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': "Method PUT no allowed"})
        try:
            instance = models.Game.objects.get(pk=pk)
        except:
            return Response({'error': 'Object not found'})
        
        serializer = serializers.GamesSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Changed': serializer.data})


class NewsViewSet(APIView):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer
