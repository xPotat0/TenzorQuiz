from .serializers import LoginUserSerializer, RegisterUserSerializer

from .serializers import RegisterUserSerializer
from .models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView


class LoginUserApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }
        serializer = LoginUserSerializer(data=data)



        if serializer.is_valid():

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)





class RegisterUserApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super(CustomTokenObtainPairView, self).post(request, *args, **kwargs)
        if 'refresh' in response.data and response.data['refresh']:
            refresh_token = response.data['refresh']
            response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        return response