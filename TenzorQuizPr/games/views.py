from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from json import loads

from .models import Game
from .models import Question
from .models import TeamQuestionAnswer
from teams.models import Team

from .serializers import GamesSerializer, SingleGameSerializer
from .serializers import QuestionsSerializer
from teams.serializers import TeamsSerializer
from .serializers import TeamQuestionAnswerSerializer

def decode_id(content):
        _content = content
        ques_list = []
        team_list = []
        for ques in _content["questions"]:
            ques_cont = QuestionsSerializer(Question.objects.get(pk=ques))
            ques_list.append(ques_cont.data)
        for team in _content["teams"]:
            team_cont = TeamsSerializer(Team.objects.get(pk=team))
            team_list.append(team_cont.data)
        _content['questions'] = ques_list
        _content['teams'] = team_list
        return _content


class GamesAPIView(CreateAPIView):
    queryset = Game.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return GamesSerializer
        else:
            return SingleGameSerializer

    
    def get(self, requset):   
        """
        Get list of all games
        """

        games = Game.objects.all()
        content = GamesSerializer(games, many=True).data
        return Response(content)
    

    def post(self, request):
        """
        Create game. Should transfer to .../games/{id}/ques/
        """
        serializer = GamesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class SingleGameAPIView(RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = SingleGameSerializer

    def get(self, requset, *args, **kwargs):   
        """Get single game with all fields"""
        pk = kwargs.get('pk', None)
        try:
            game = Game.objects.get(id=pk)
        except:
            return Response({'error': 'Object not found'})
            
        content = SingleGameSerializer(game).data

        content = decode_id(content)
        return Response(content)
    
    def put(self, request, *args, **kwargs):
        """
        Change existed game by id
        """
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
        return Response(serializer.data)


    
class QuestionsAPIView(CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = QuestionsSerializer

    def post(self, request, *args, **kwargs):
        """Create question and automaticly add to current game"""
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
    

class PlayGameAPIView(CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = TeamQuestionAnswerSerializer

    def change_game_status(game):
        Game.objects.filter(pk=GamesSerializer(game).data['id']).update(is_over=True)
        return 


    def post(self, request, *args, **kwargs):
        """Change team's answer. If there is no object of answer then create one"""
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
        return Response(dat)
