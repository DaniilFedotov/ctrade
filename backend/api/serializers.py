from rest_framework.serializers import ModelSerializer

from ..deals.models import Deal, Trader


class DealSerializer(ModelSerializer):
    """Serializer for the deal model."""
    class Meta:
        model = Deal
        fields = ('id', 'opening_date', 'closed', 'ticker',
                  'purchase_price', 'selling_price', 'trader',)
        read_only_fields = ('id',)


class TraderSerializer(ModelSerializer):
    """Serializer for the trader model."""
    class Meta:
        model = Trader
        fields = ('id', 'creation_date', 'working', 'initial_deposit',
                  'current_deposit', 'revenue', 'market',)
        read_only_fields = ('id',)
