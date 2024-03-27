from rest_framework.viewsets import ModelViewSet

from deals.models import Deal, Trader, Grid, Level, Ticker
from .serializers import (DealSerializer, TraderSerializer,
                          GridSerializer, LevelSerializer,
                          TickerSerializer)


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


class LevelViewSet(ModelViewSet):
    """Viewset for the level model."""
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class TickerViewSet(ModelViewSet):
    """Viewset for the ticker model."""
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
