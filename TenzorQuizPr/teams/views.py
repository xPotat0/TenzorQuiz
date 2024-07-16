from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TeamSerializer, TeamListSerializer, TeamCreateSerializer, TeamUpdateSerializer, \
    TeamJoinSerializer
from teams.models import Team


class TeamsListAPIView(APIView):
    queryset = Team.objects.all()

    @swagger_auto_schema(
        operation_description="Получение списка всех команд в порядке убывания набранных очков",
        responses={200: TeamListSerializer(many=True)}
    )
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamListSerializer(teams, many=True)
        return Response({'teams': serializer.data})

    @swagger_auto_schema(
        operation_description="Создание новой команды. Обязательные поля - captain_id и team_name",
        request_body=TeamCreateSerializer,
        responses={200: TeamCreateSerializer()}
    )
    def post(self, request):
        serializer = TeamCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamAPIView(APIView):
    queryset = Team.objects.all()

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
        responses={201: TeamUpdateSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method not allowed"})
        try:
            instance = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "detail": f"Команды c id {pk} не существует "
            })

        serializer = TeamUpdateSerializer(data=request.data, instance=instance, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='patch',
    operation_description="Добавление участника в команду. Обязательное поле - user_id",
    request_body=TeamJoinSerializer,
    responses={200: TeamJoinSerializer()}
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
        serializer.add_member(user_id=user_id, team=team)
        return Response({'team_id': pk,
                        'user_id': user_id})


#
# @swagger_auto_schema(
#     method='patch',
#     operation_description="Join team",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'user_id': openapi.Schema(type=openapi.TYPE_INTEGER)}),
#     responses={200: openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'team_id': openapi.Schema(type=openapi.TYPE_INTEGER),
#             'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
#         })
#     }
# )
# @api_view(['PATCH'])
# def join_team(request, *args, **kwargs):
#     pk = kwargs.get("pk", None)
#     if not pk:
#         return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     try:
#         team = Team.objects.get(pk=pk)
#     except Team.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND, data={
#             "detail": f"Команды c id {pk} не существует "
#         })
#
#     user_id = request.data.get('user_id')
#     if not user_id:
#         return Response({"error": "Поле user_id обязательно"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     serializer = TeamJoinSerializer(partial=True)
#     serializer.add_member(user_id=user_id, team=team)
#
#     return Response({'team_id': pk,
#                      'user_id': user_id})


