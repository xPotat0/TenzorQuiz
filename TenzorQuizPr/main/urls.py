from django.contrib import admin
from django.urls import path, include
from .views import RegisterView, CustomTokenObtainPairView, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/v1/customtoken/', CustomTokenObtainPairView.as_view(), name='customtoken'),
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/register/', RegisterView.as_view()),
]
