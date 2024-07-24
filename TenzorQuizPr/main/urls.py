from django.urls import path
from .views import RegisterView, LoginView, LogoutView, RefreshTokenView, UserProfileView

urlpatterns = [
    path('api/v1/auth/login/', LoginView.as_view(), name='login'),
    path('api/v1/auth/register/', RegisterView.as_view(), name='register'),
    path('api/v1/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/auth/refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('api/v1/user/', UserProfileView.as_view(), name='user'),
]