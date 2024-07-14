from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from json import loads

from .models import Game
from .models import Question
from .models import TeamQuestionAnswer
from teams.models import Team

from .serializers import GamesSerializer
from .serializers import QuestionsSerializer
from teams.serializers import TeamsSerializer
from .serializers import TeamQuestionAnswerSerializer



# Create your views here.
class GamesAPIView(APIView):
    def get(self, requset, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            try:
                instance = Game.objects.get(pk=pk)
            except:
                return Response({'error': 'Object not found'})
            
            return Response({'Status': 'Accepted', 'Content': GamesSerializer(instance).data})

        games = Game.objects.all()
        content = GamesSerializer(games, many=True).data
        for game in content:
            ques_list = []
            team_list = []
            for ques in game["questions"]:
                ques_cont = QuestionsSerializer(Question.objects.get(pk=ques))
                ques_list.append(ques_cont.data)
            for team in game["teams"]:
                team_cont = TeamsSerializer(Team.objects.get(pk=team))
                team_list.append(team_cont.data)
            game['questions'] = ques_list
            game['teams'] = team_list
        return Response({'Status': 'Accepted', 'Content': content})
    

    def post(self, request):
        serializer = GamesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'New object created': serializer.data})



    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': "Method PUT no allowed"})
        try:
            instance = Game.objects.get(pk=pk)
        except:
            return Response({'error': 'Object not found'})
        
        serializer = GamesSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Changed': serializer.data})


    
class QuestionsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        game_id = kwargs.get('game_id', None)

        if not game_id:
            return Response({'error': 'Method PUT no allowed'})

        try:
            game = Game.objects.get(id=game_id)
        except:
            return Response({'error': 'Game not exists'})
        
        
        ques_serializer = QuestionsSerializer(data=request.data)
        ques_serializer.is_valid(raise_exception=True)
        question = ques_serializer.save()


        game.questions.add(question)
        game.save()

        return Response({'New question created': ques_serializer.data})
    

class PlayGameAPIView(APIView):
    def change_game_status(game):
        Game.objects.filter(pk=GamesSerializer(game).data['id']).update(is_over=True)
        return 

    #Creating Teams X Questions records in Team question answer table
    def post(self, request, *args, **kwargs):
        game_id = kwargs.get('game_id', None)

        if not game_id:
            return Response({'error': 'Method PUT no allowed'})
        
        try:
            game = Game.objects.get(id=game_id)
        except:
            return Response({'error': 'Game not exists'})

        decoded_request = loads(request.body.decode('utf-8'))
        is_over = False
        try:
            is_over = decoded_request['is_over']
        except:
            ...
        
        if (is_over):
            PlayGameAPIView.change_game_status(game)
            return Response({'Status': 'game over'})

        team = Team.objects.get(pk=decoded_request['team_id'])
        question = Question.objects.get(pk=decoded_request['question_id'])

        obj, created = TeamQuestionAnswer.objects.update_or_create(game=game, team=team, question=question, defaults={'is_correct': decoded_request['is_correct']})
        dat = TeamQuestionAnswerSerializer(obj).data
        return Response({'Status': 'answer accepted', 'object': created, 'answer': dat})
