from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import main.models as models
import main.serializers as serializers

# Create your views here.
class TeamsAPIView(APIView):
    def getAll():
        return Response({'Status': 'Accepted', 'Content': list(models.Team.objects.all().values())})

    def get(self, request):
        if True:
            response = TeamsAPIView.getAll()
        return response
