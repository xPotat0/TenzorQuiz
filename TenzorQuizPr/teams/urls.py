from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/v1/teams/', views.TeamsAPIView.as_view()),
]