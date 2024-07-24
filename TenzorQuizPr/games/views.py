from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
import settings

from drf_yasg.utils import swagger_auto_schema

from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django .db.models import Q
import rest_framework_simplejwt.settings
import jwt
import rest_framework_simplejwt.tokens
from json import loads

from .models import Game, Question, TeamQuestionAnswer
from teams.models import Team
from main.models import User

from .serializers import GamesSerializer, SingleGameSerializer, QuestionsSerializer, TeamQuestionAnswerSerializer, DeleteQuestionSerializer, TeamToGameSerializer
from teams.serializers import TeamsSerializer, TeamSerializer
from main.serializers import UserSerializer

from django.db.models import IntegerField
from django.db.models.functions import Cast
from drf_yasg import openapi


def decode_id(content):
        _content = content
        ques_list = []
        team_list = []
        for ques in _content["game_questions"]:
            ques_cont = QuestionsSerializer(Question.objects.get(pk=ques))
            ques_list.append(ques_cont.data)
        for team in _content["game_teams"]:
            team_cont = TeamsSerializer(Team.objects.get(id=team))
            team_list.append(team_cont.data)
        _content['game_questions'] = ques_list
        _content['game_teams'] = team_list
        return _content


class ScheduledGamesAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Получить список запланированных игр",
        responses={
            200: openapi.Response(
                description="Успешный ответ с списком запланированных игр",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'game_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'game_description': openapi.Schema(type=openapi.TYPE_STRING),
                            'game_date': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                            'game_status': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                )
            )
        }
    )
    def get(self, request):
        games = Game.objects.filter(game_status='planned')
        serializer = GamesSerializer(games, many=True)
        return Response(serializer.data)


def checkGameStatus(game, needStatus):
    return SingleGameSerializer(game).data['game_status'] in needStatus

def makeAllCheckes(kwargs, attributeName, objModel, checkGameForStatus = False, statuses = ['planned']):
        obj_id = kwargs.get(attributeName, None)   
        if not obj_id:
            return (None, Response({'error': 'Method no allowed'}, status=status.HTTP_403_FORBIDDEN))
        
        try:
            obj = objModel.objects.get(id=obj_id)
        except:
            return (None, Response({'error': str(objModel) + ' not exists'}, status=status.HTTP_404_NOT_FOUND))
        


        if checkGameForStatus:
            if not checkGameStatus(obj, statuses):
                return (None, Response({'error': 'Cannot change already played/ing game'}, status=status.HTTP_406_NOT_ACCEPTABLE))
        
        return (obj, None)

def getTeamsPoints(game):
    answers = TeamQuestionAnswer.objects.filter(game_id=game)
    content = TeamQuestionAnswerSerializer(answers, many=True).data
    
    teams_id = {}
    for team in SingleGameSerializer(game).data['game_teams']:
        teams_id[team] = 0
        
    for record in content:
        teams_id[record['team_id']] += record['answer_score']

    content.append({'scores': teams_id})
    return content

def addScoreToTeams(game):
    content = getTeamsPoints(game)
    scores = content[len(content) - 1]

    for team_id, score in dict(scores['scores']).items():
        team = Team.objects.get(id=int(team_id))
        team.points += score
        team.played_games += 1
        team.save(update_fields=['points', 'played_games'])

    

    return None


class GamesAPIView(CreateAPIView):
    queryset = Game.objects.all()
    filter_backends = [filters.SearchFilter]
    permission_classes = [AllowAny]

 
    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return GamesSerializer
        else:
            return SingleGameSerializer


    def get(self, request, *args, **kwargs):   
        """
        Получение списка всех игр
        """
        search = request.query_params.get('search')
        order = request.query_params.get('ordering')
        page = request.query_params.get('page')
        if search is None:
            search = ''  
        if order is None:
            order = '-game_date'
        if page is None:
            page = 1
        page = int(page)

        words = search.strip().split() # можно разбить регуляркой
        or_contains = Q()
        for word in words:
            or_contains |= Q(game_name__icontains=word)
            
        games = Game.objects.filter(or_contains).order_by(order).all()[(page-1)*10:page*10]
        content = GamesSerializer(games, many=True).data
        return Response(content)
    


    def post(self, request, *args, **kwargs):
        """
        Создание игры. Должно переводить в  .../games/{game_id}/ques/
        """
        #print(request.headers)
        #decoded_id = 2
        #request.data['game_creator'] = decoded_id

        serializer = SingleGameSerializer(data=request.data)
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
        checks = makeAllCheckes(kwargs, 'game_id', Game)

        if checks[1] != None:
            return checks[1]
        else:
            game = checks[0]

            
        content = SingleGameSerializer(game).data

        content = decode_id(content)
        return Response(content)
    

    def put(self, request, *args, **kwargs):
        """
        Изменить существующую игру по ID
        """
        checks = makeAllCheckes(kwargs, 'game_id', Game, checkGameForStatus=True)

        if checks[1] != None:
            return checks[1]
        else:
            game = checks[0]

        serializer = GamesSerializer(data=request.data, instance=game)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class QuestionsAPIView(CreateAPIView):
    queryset = Game.objects.all()
    #authentication_classes = [SessionAuthentication, BaseAuthentication]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionsSerializer
        else:
            return DeleteQuestionSerializer


    def post(self, request, *args, **kwargs):
        """Создать вопрос и автоматически добавить его в игру"""
        game_id = kwargs.get('game_id', None)
        
        checks = makeAllCheckes(kwargs, 'game_id', Game, checkGameForStatus=True)

        if checks[1] != None:
            return checks[1]
        else:
            game = checks[0]
        print(request.data)

        for ques in request.data:
            ques_serializer = QuestionsSerializer(data=ques)
            ques_serializer.is_valid(raise_exception=True)
            question = ques_serializer.save()
            game.game_questions.add(question)
        
        game.save()

        return Response(status=status.HTTP_200_OK)
    


    @swagger_auto_schema(
        request_body=DeleteQuestionSerializer,
        responses={204: DeleteQuestionSerializer}
    )
    def delete(self, request, *args, **kwargs):
        """Удалить вопрос из игры"""
        checks = makeAllCheckes(kwargs, 'game_id', Game, checkGameForStatus=True)

        if checks[1] != None:
            return checks[1]
        else:
            game = checks[0]
        
        try:
            decoded_request = loads(request.body.decode('utf-8'))
            ques = Question.objects.get(pk=decoded_request['ques_id'])
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
        checks = makeAllCheckes(kwargs, 'game_id', Game)

        if checks[1] != None:
            return checks[1]
        else:
            game = checks[0]


        content = getTeamsPoints(game)
        return Response(content)



    def post(self, request, *args, **kwargs):
        """Поменять ответ команды. Если объекта ответа нет в базе, то он создаётся"""
        checks = makeAllCheckes(kwargs, 'game_id', Game, checkGameForStatus=True, statuses=['planned', 'active'])

        if checks[1] != None:
            return checks[1]
        else:
            game = checks[0]
        
        decoded_request = loads(request.body.decode('utf-8'))      

        if game.game_status == 'planned':
            game.game_status = 'active'
            game.save(update_fields=['game_status'])

        try:
            if decoded_request['status'] == 'finished':
                game.game_status = 'finished'
                game.save(update_fields=['game_status'])
                addScoreToTeams(game)
                return Response({'status': 'Game finished'}) 
        except:
            ...


        team = Team
        try:
            team = Team.objects.get(id=decoded_request['team_id'])
        except:
            return Response({'error': 'Team not exists'}, status=status.HTTP_404_NOT_FOUND)

        question = Question        
        try:
            question = Question.objects.get(id=decoded_request['question_id'])
        except:
            return Response({'error': 'Question not exists'}, status=status.HTTP_404_NOT_FOUND)

        is_correct = question.question_correct_answer == decoded_request['answer_team_answer']

        obj, created = TeamQuestionAnswer.objects.update_or_create(
            game_id=game,
            team_id=team, 
            question_id=question, 
            defaults={'answer_is_correct': is_correct, 'answer_team_answer' : decoded_request['answer_team_answer'], 'answer_score': decoded_request['answer_score']})
        dat = TeamQuestionAnswerSerializer(obj).data
        return Response(dat)


class GameAddTeamAPIView(CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamToGameSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_user = request.user
            team = Team
            try:
                team = Team.objects.get(captain_id=auth_user.id)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response({'team_id': TeamsSerializer(team).data['team_id']}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        """Записать команду на игру"""
        checks = makeAllCheckes(kwargs, 'game_id', Game, checkGameForStatus=True)

        if checks[1] != None:
            return checks[1]
        else:
            game = checks[0]

        
        decoded_request = loads(request.body.decode('utf-8'))
        user_id = decoded_request['user_id']
        
        try:
            team = Team.objects.get(captain_id=user_id)

        except:
            return Response({'error': 'User does not have team'}, status=status.HTTP_404_NOT_FOUND)

        game.game_teams.add(team)

        game.save()

        return Response({'status': 'success'})
    
    @swagger_auto_schema(
        request_body=TeamToGameSerializer,
        responses={204: TeamToGameSerializer}
    )
    def delete(self, request, *args, **kwargs):
        """Удалить команду из игры"""
        checks = makeAllCheckes(kwargs, 'game_id', Game, checkGameForStatus=True)

        if checks[1] != None:
            return checks[1]
        else:
            game = checks[0]

        
        try:
            decoded_request = loads(request.body.decode('utf-8'))
            team = Team.objects.get(pk=decoded_request['team_id'])
        except:
            return Response({'error': 'Game does not have team'}, status=status.HTTP_404_NOT_FOUND)

        game.game_teams.remove(team)
        return Response(status=status.HTTP_204_NO_CONTENT)
    #Убирать в поиске начальные и конечные пробелы
