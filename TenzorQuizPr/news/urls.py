from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/v1/news/', views.NewsAPIView.as_view()),
]