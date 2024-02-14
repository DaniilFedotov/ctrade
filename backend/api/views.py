from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from deals.models import Deal, Trader
from .serializers import DealSerializer, TraderSerializer


class DealViewSet(ModelViewSet):
    """Viewset for the deal model."""
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class TraderViewSet(ModelViewSet):
    """Viewset for the trader model."""
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer

