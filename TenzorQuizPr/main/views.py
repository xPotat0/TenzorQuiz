from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer, \
    CustomTokenRefreshSerializer
from .models import User

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


class RegisterView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        request_body=RegisterSerializer,
        responses={201: ''}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Авторизация",
        request_body=CustomTokenObtainPairSerializer,
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tokens': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    }),
                'user': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            })},
    )
    def post(self, request, *args, **kwargs):
        response = Response(data={
            "tokens": {},
            "user": None})

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data['tokens']
        auth_user = serializer.validated_data['user']

        serializer = UserSerializer(auth_user)
        refresh_token = tokens['refresh']
        access_token = tokens['access']
        # response.set_cookie(
        #     key='refresh_token',
        #     value=str(refresh_token),
        #     httponly=True,
        #     secure=True,
        #     samesite='None',
        #     max_age=7 * 24 * 60 * 60 * 1000
        # )
        # response.data['refresh_token'] = str(refresh_token)
        # response.data['access_token'] = str(access_token)
        response.data['tokens'] = {
            "refresh_token": str(refresh_token),
            "access_token": str(access_token),
        }
        response.data['user'] = serializer.data
        return response


class RefreshTokenView(APIView):
    serializer_class = CustomTokenRefreshSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Обновление токенов",
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tokens': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    }),
                'user': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            })},
    )
    def get(self, request, *args, **kwargs):
        # response = Response(data={"access_token": None,
        #                           "user": None})
        response = Response(data={
            "tokens": {},
            "user": None})
        # refresh_token = request.COOKIES.get('refresh_token')
        refresh_token = request.query_params.get('token')
        if not refresh_token:
            return Response(data={"detail": "Пользователь не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data['user']
        new_refresh_token = data['refresh']
        new_access_token = data['access']
        # user = request.user
        serializer = UserSerializer(user)
        # new_token = RefreshToken.for_user(user)
        # new_token.payload.update({'role': user.role})
        # response.set_cookie(
        #     key='refresh_token',
        #     value=new_refresh_token,
        #     httponly=True,
        #     secure=True,
        #     samesite='None',
        #     max_age=7 * 24 * 60 * 60 * 1000
        # )
        # response.data['refresh_token'] = new_refresh_token
        # response.data['access_token'] = new_access_token
        response.data['tokens'] = {
            "refresh_token": new_refresh_token,
            "access_token": new_access_token,
        }
        response.data['user'] = serializer.data
        return response


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh_token": openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: ''}
    )
    def post(self, request):
        try:
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            refresh_token = request.data.get('refresh_token')

            token = RefreshToken(refresh_token)
            token.blacklist()
            # response.delete_cookie('refresh_token')
            return response
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
