from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsView, NewsAndScheduledGamesAPIView

router = DefaultRouter()
router.register(r'news', NewsView)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/news-and-scheduled-games/', NewsAndScheduledGamesAPIView.as_view(), name='news-and-scheduled-games'),
]
