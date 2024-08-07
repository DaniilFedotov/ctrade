from rest_framework.viewsets import ModelViewSet

from deals.models import Deal, Trader, Grid, Level, Ticker
from .serializers import (DealSerializer, TraderSerializer,
                          CreateTraderSerializer, GridSerializer,
                          CreateGridSerializer, LevelSerializer,
                          TickerSerializer)


class DealViewSet(ModelViewSet):
    """Viewset for the deal model."""
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class TraderViewSet(ModelViewSet):
    """Viewset for the trader model."""
    queryset = Trader.objects.all()

    def get_serializer_class(self):
        """Gets the required serializer."""
        if self.request.method == "POST":
            return CreateTraderSerializer
        return TraderSerializer


class GridViewSet(ModelViewSet):
    """Viewset for the grid model."""
    queryset = Grid.objects.all()

    def get_serializer_class(self):
        """Gets the required serializer."""
        if self.request.method == "POST":
            return CreateGridSerializer
        return GridSerializer


class LevelViewSet(ModelViewSet):
    """Viewset for the level model."""
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class TickerViewSet(ModelViewSet):
    """Viewset for the ticker model."""
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
