from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DealViewSet, TraderViewSet

app_name = 'api'

router = DefaultRouter()
router.register('deals', DealViewSet, basename='deals')
router.register('traders', TraderViewSet, basename='traders')

urlpatterns = [
    path('', include(router.urls), name='api-root'),
]
