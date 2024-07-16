"""
URL configuration for TenzorQuizPr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main.urls import urlpatterns as main_url
from games.urls import urlpatterns as games_url
from teams.urls import urlpatterns as teams_url
from news.urls import urlpatterns as news_url

#from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version='v1',
        description="API documentation for your project",
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api_schema', get_schema_view(title='API schema', description='List of API\'s'), name='api_schema'),
    # path('swagger-ui/', TemplateView.as_view(template_name='docs.html', extra_context={'schema_url':'api_schema'}), name='swagger-ui'),
    path('swagger-ui/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('main.urls')),
    ]

urlpatterns += main_url
urlpatterns += games_url
urlpatterns += teams_url
urlpatterns += news_url