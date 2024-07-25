from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ScheduledGamesAPIView, PlannedGameDetailAPIView

urlpatterns = [
        path('api/v1/games/', views.GamesAPIView.as_view()),
        path('api/v1/games/<int:game_id>/', views.SingleGameAPIView.as_view()),
        path('api/v1/games/<int:game_id>/ques/', views.QuestionsAPIView.as_view()),
        path('api/v1/games/<int:game_id>/play/', views.PlayGameAPIView.as_view()),
        path('api/v1/games/<int:game_id>/teams/', views.GameAddTeamAPIView.as_view()),
        path('api/v1/scheduled-games/', ScheduledGamesAPIView.as_view(), name='scheduled-games'),
        path('api/v1/planned-game/<int:id>/', PlannedGameDetailAPIView.as_view(), name='planned-game-detail'),
]
