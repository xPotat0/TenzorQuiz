from django.contrib import admin
from django.urls import path, include
from .views import LoginUserApiView, CustomTokenObtainPairView, RegisterUserApiView

urlpatterns = [
    path('api/v1/login/', LoginUserApiView.as_view()),
    path('api/v1/token/', CustomTokenObtainPairView.as_view()),
    path('api/v1/register/', RegisterUserApiView.as_view()),
]