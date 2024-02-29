from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from deals.models import Deal, Trader, Grid
from .serializers import (DealSerializer, TraderSerializer,
                          GridSerializer)


class DealViewSet(ModelViewSet):
    """Viewset for the deal model."""
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class TraderViewSet(ModelViewSet):
    """Viewset for the trader model."""
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer


class GridViewSet(ModelViewSet):
    """Viewset for the grid model."""
    queryset = Grid.objects.all()
    serializer_class = GridSerializer
