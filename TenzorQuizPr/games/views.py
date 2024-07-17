from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from json import loads

from .models import Game, Question, TeamQuestionAnswer
from teams.models import Team

from .serializers import GamesSerializer, SingleGameSerializer, QuestionsSerializer, TeamQuestionAnswerSerializer, DeleteQuestionSerializer
from teams.serializers import TeamsSerializer

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
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return GamesSerializer
        else:
            return SingleGameSerializer

    
    def get(self, requset):   
        """
        Получение списка всех игр
        """

        games = Game.objects.all()
        content = GamesSerializer(games, many=True).data
        return Response(content)
    

    def post(self, request):
        """
        Создание игры. Должно переводить в  .../games/{id}/ques/
        """
        serializer = GamesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class SingleGameAPIView(RetrieveAPIView):
    queryset = Game.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return GamesSerializer
        else:
            return SingleGameSerializer
        



    def get(self, requset, *args, **kwargs):   
        """Получение одной игры со всеми полями"""
        pk = kwargs.get('pk', None)
        try:
            game = Game.objects.get(id=pk)
        except:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
            
        content = SingleGameSerializer(game).data

        content = decode_id(content)
        return Response(content)
    
    def put(self, request, *args, **kwargs):
        """
        Изменить существующую игру по ID
        """
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': "Method PUT no allowed"})
        try:
            instance = Game.objects.get(pk=pk)
        except:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GamesSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    
class QuestionsAPIView(CreateAPIView):
    queryset = Game.objects.all()
    authentication_classes = [SessionAuthentication, BaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionsSerializer
        else:
            return DeleteQuestionSerializer



    def post(self, request, *args, **kwargs):
        """Создать вопрос и автоматически добавить его в игру"""
        game_id = kwargs.get('game_id', None)

        if not game_id:
            return Response({'error': 'Method PUT no allowed'})

        try:
            game = Game.objects.get(id=game_id)
        except:
            return Response({'error': 'Game not exists'}, status=status.HTTP_404_NOT_FOUND)
        
        
        ques_serializer = QuestionsSerializer(data=request.data)
        ques_serializer.is_valid(raise_exception=True)
        question = ques_serializer.save()


        game.questions.add(question)
        game.save()

        return Response(ques_serializer.data)
    
    @swagger_auto_schema(
        request_body=DeleteQuestionSerializer,
        responses={204: DeleteQuestionSerializer}
    )
    def delete(self, request, *args, **kwargs):
        """Удалить вопрос из игры"""
        game_id = kwargs.get('game_id', None)

        if not game_id:
            return Response({'error': 'Method PUT no allowed'})

        try:
            game = Game.objects.get(id=game_id)
        except:
            return Response({'error': 'Game not exists'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            decoded_request = loads(request.body.decode('utf-8'))
            ques = Question.objects.get(pk=decoded_request['id'])
        except:
            return Response({'error': 'No such question'}, status=status.HTTP_404_NOT_FOUND)
        
        ques.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    

class PlayGameAPIView(CreateAPIView):
    queryset = TeamQuestionAnswer.objects.all()
    serializer_class = TeamQuestionAnswerSerializer
    permission_classes = [AllowAny]

    def change_game_status(game):
        Game.objects.filter(pk=GamesSerializer(game).data['id']).update(is_over=True)
        return 

    def get(self, request, *args, **kwargs):
        """Получение всех записанных ответов команд"""
        game_id = kwargs.get('game_id', None)
        if not game_id:
            return Response({'error': 'Method GET no allowed'})
        
        try:
            game = Game.objects.get(id=game_id)
        except:
            return Response({'error': 'Game not exists'}, status=status.HTTP_404_NOT_FOUND)
        
        answers = TeamQuestionAnswer.objects.filter(game=game)
        content = TeamQuestionAnswerSerializer(answers, many=True).data
        print(content)

        return Response(content)


    def post(self, request, *args, **kwargs):
        """Поменять ответ команды. Если объекта ответа нет в базе, то он создаётся"""
        game_id = kwargs.get('game_id', None)
        if not game_id:
            return Response({'error': 'Method PUT no allowed'})
        
        try:
            game = Game.objects.get(id=game_id)
        except:
            return Response({'error': 'Game not exists'}, status=status.HTTP_404_NOT_FOUND)

        decoded_request = loads(request.body.decode('utf-8'))
        is_over = False
        try:
            is_over = decoded_request['is_over']
        except:
            ...
        
        if (is_over):
            PlayGameAPIView.change_game_status(game)
            return Response({'Status': 'game over'})

        team = Team.objects.get(pk=decoded_request['team'])
        question = Question.objects.get(pk=decoded_request['question'])

        obj, created = TeamQuestionAnswer.objects.update_or_create(game=game, team=team, question=question, defaults={'is_correct': decoded_request['is_correct']})
        dat = TeamQuestionAnswerSerializer(obj).data
        return Response(dat)
