from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsView

router = DefaultRouter()
router.register(r'news', NewsView)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
