from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
def index(request):
    return HttpResponse("<h4>Основная страница</h4>")

