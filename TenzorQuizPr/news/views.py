from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import News
from .serializers import NewsSerializer
from rest_framework.serializers import ListSerializer

# Create your views here.
def index(request):
    return HttpResponse("<h4>Страница новостей</h4>")

class NewsAPIView(APIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer