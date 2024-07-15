from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Team
from .serializers import TeamsSerializer

# Create your views here.
class TeamsAPIView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamsSerializer
    def getAll():
        return Response({'Status': 'Accepted', 'Content': list(Team.objects.all().values())})

    def get(self, request):
        if True:
            response = TeamsAPIView.getAll()
        return response
