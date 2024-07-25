from datetime import datetime

from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from games.models import Game
from games.serializers import GamesSerializer
from .models import News
from .serializers import NewsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import filters
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination


class NewsView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny] 

    @swagger_auto_schema(
        operation_description="Получить список всех новостей",
        responses={200: openapi.Response(
            description="Успешный ответ с списком новостей",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'image': openapi.Schema(type=openapi.TYPE_FILE),
                    }
                )
            )
        )}
    )
    def list(self, request, *args, **kwargs):
        """
        Получает список всех новостей.
        """

        search = request.query_params.get('search')
        page = request.query_params.get('page')
        if search is None:
            search = ''
        if page is None:
            page = 1
        page = int(page)

        words = search.strip().split() # можно разбить регуляркой
        or_contains = Q()
        for word in words:
            or_contains |= Q(news_name__icontains=word)

        news = News.objects.filter(or_contains).all()[(page-1)*10:page*10]
        content = NewsSerializer(news, many=True).data

        return super().list(request, content, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую новость",
        request_body=NewsSerializer,
        responses={
            201: openapi.Response(
                description="Создана новая новость",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={field: openapi.Schema(type=openapi.TYPE_STRING) for field in NewsSerializer().fields}
                )
            ),
            403: openapi.Response(
                description="Отказ в доступе. Только ведущие могут создавать новости."
            )
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Создает новую новость. Доступно только для пользователей с ролью 'ведущий'.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить информацию о конкретной новости",
        responses={
            200: openapi.Response(
                description="Успешный ответ с информацией о новости",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={field: openapi.Schema(type=openapi.TYPE_STRING) for field in NewsSerializer().fields}
                )
            ),
            404: openapi.Response(
                description="Новость не найдена"
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Получает информацию о конкретной новости по её ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить информацию о конкретной новости",
        request_body=NewsSerializer,
        responses={
            200: openapi.Response(
                description="Успешное обновление новости",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={field: openapi.Schema(type=openapi.TYPE_STRING) for field in NewsSerializer().fields}
                )
            ),
            404: openapi.Response(
                description="Новость не найдена"
            )
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Обновляет всю информацию о конкретной новости по её ID.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить информацию о конкретной новости",
        request_body=NewsSerializer,
        responses={
            200: openapi.Response(
                description="Успешное частичное обновление новости",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={field: openapi.Schema(type=openapi.TYPE_STRING) for field in NewsSerializer().fields}
                )
            ),
            404: openapi.Response(
                description="Новость не найдена"
            )
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет информацию о конкретной новости по её ID.
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить новость",
        responses={
            204: openapi.Response(
                description="Новость успешно удалена"
            ),
            404: openapi.Response(
                description="Новость не найдена"
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Удаляет конкретную новость по её ID.
        """
        return super().destroy(request, *args, **kwargs)
