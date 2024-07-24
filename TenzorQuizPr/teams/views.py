from django.db.models import F, Case, When, FloatField, Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny, IsAuthenticated

from main.models import User
from .serializers import TeamSerializer, TeamListSerializer, TeamCreateSerializer, TeamUpdateSerializer, \
    TeamJoinSerializer
from teams.models import Team


class TeamsListAPIView(APIView):
    queryset = Team.objects.all()

    @swagger_auto_schema(
        operation_description="Получение списка всех команд в порядке убывания занимаемых мест",
        responses={200: TeamListSerializer(many=True)}
    )
    def get(self, request):
        search = request.query_params.get('search')
        order = get_order(request)
        page = request.query_params.get('page')
        if search is None:
            search = ''
        if page is None:
            page = 1
        page = int(page)
        teams = set_team_places()
        words = search.strip().split()
        or_contains = Q()
        for word in words:
            or_contains |= Q(team_name__icontains=word)
        teams_filtered = teams.filter(or_contains).order_by(order).all()[(page - 1) * 10:page * 10]
        serializer = TeamListSerializer(teams_filtered, many=True)
        return Response({'teams': serializer.data})

    @swagger_auto_schema(
        operation_description="Создание новой команды. Обязательные поля - captain_id и team_name",
        request_body=TeamCreateSerializer,
        responses={201: TeamSerializer()}
    )
    def post(self, request):
        serializer = TeamCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            team = serializer.save()
            team_repr = TeamSerializer(team)
            return Response(team_repr.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamAPIView(APIView):
    queryset = Team.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Получение информации о команде по ID",
        responses={200: TeamSerializer()}
    )
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "detail": f"Команды c id {pk} не существует "
            })

        serializer = TeamSerializer(team)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Удаление команды по ID"
    )
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "detail": f"Команды c id {pk} не существует "
            })
        team.delete()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Изменение названия или описания команды",
        request_body=TeamUpdateSerializer,
        responses={201: TeamSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method not allowed"})
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "detail": f"Команды c id {pk} не существует "
            })

        serializer = TeamUpdateSerializer(data=request.data, instance=team, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            team_repr = TeamSerializer(team)
            return Response(data=team_repr.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='patch',
    operation_description="Добавление участника в команду. Обязательное поле - user_id",
    request_body=TeamJoinSerializer,
    responses={200: TeamSerializer()}
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def join_team(request, *args, **kwargs):
    pk = kwargs.get("pk", None)
    if not pk:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={
            "detail": f"Команды c id {pk} не существует "
        })
    serializer = TeamJoinSerializer(data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        user_id = request.data.get('user_id')
        team = serializer.add_member(user_id=user_id, team=team)
        team_repr = TeamSerializer(team)
        return Response(data=team_repr.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_team(request, *args, **kwargs):
    pk = kwargs.get("pk", None)
    if not pk:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    auth_user = request.user
    team = User.objects.get(id=auth_user.id).teams.all().filter(id=pk).first()
    if not team:
        return Response(status=status.HTTP_404_NOT_FOUND, data={f"Вы не состоите в данной команде"})
    if team.captain_id == auth_user.id:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"Капитан не может выходить из команды"})
    team.team_members.remove(auth_user)
    team.save()
    team_repr = TeamSerializer(team)
    return Response(status=status.HTTP_200_OK, data=team_repr.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def my_teams(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'Авторизуйтесь, чтобы просмотреть свои команды'})
    search = request.query_params.get('search')
    order = get_order(request)
    page = request.query_params.get('page')
    if search is None:
        search = ''
    if page is None:
        page = 1
    page = int(page)
    words = search.strip().split()
    or_contains = Q()
    for word in words:
        or_contains |= Q(team_name__icontains=word)
    auth_user = request.user
    user_teams = User.objects.get(id=auth_user.id).teams.all()
    user_teams_filtered = user_teams.filter(or_contains).order_by(order).all()[(page - 1) * 10:page * 10]
    data = TeamListSerializer(user_teams_filtered, many=True).data
    return Response({'user_teams': data})


def get_order(request):
    order = request.query_params.get('ordering')
    if order is None:
        return 'place'
    elif order == 'points':
        return '-points'
    elif order == 'creation_date':
        return '-creation_date'
    elif order == 'played_games':
        return '-played_games'
    elif order == 'team_name' or order == 'place':
        return order


def set_team_places():
    teams = Team.objects.annotate(
        av_points=Case(
            When(played_games__gt=0, then=F('points') / F('played_games')),
            default=0,
            output_field=FloatField()
        )).order_by('-av_points')
    for index, val in enumerate(teams):
        val.place = index + 1
        val.save()
    return teams

