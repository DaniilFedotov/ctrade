from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (DealViewSet, TraderViewSet,
                    GridViewSet, LevelViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('deals', DealViewSet, basename='deals')
router.register('traders', TraderViewSet, basename='traders')
router.register('grids', GridViewSet, basename='grids')
router.register('levels', LevelViewSet, basename='levels')

urlpatterns = [
    path('', include(router.urls), name='api-root'),
]
