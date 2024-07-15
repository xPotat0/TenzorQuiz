from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
        path('api/v1/games/', views.GamesAPIView.as_view()),
        path('api/v1/games/<int:pk>/', views.SingleGameAPIView.as_view()),
        path('api/v1/games/<int:game_id>/ques/', views.QuestionsAPIView.as_view()),
        path('api/v1/games/<int:game_id>/play/', views.PlayGameAPIView.as_view()),
]