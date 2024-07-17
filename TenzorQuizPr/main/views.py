from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .serializers import UserSerializer, LoginSerializer
from .models import User

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login



#User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)

        user.access_token = str(refresh.access_token)
        user.save()

        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(login=request.data['username'])

        user.access_token = response.data['access']
        user.save()

        response.set_cookie(
            key='refresh_token',
            value=response.data['refresh'],
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        return response


class LoginView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        login_data = request.data

        username = login_data.get('username')  # Проверка наличия ключа 'login'
        password = login_data.get('password')



        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # В этом месте можно создать и вернуть access_token и refresh_token
            return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)