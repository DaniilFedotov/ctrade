from rest_framework.serializers import ModelSerializer

from deals.models import (Deal, Trader, Token, Currency,
                          Grid, TradingPair)


class TokenSerializer(ModelSerializer):
    """Serializer for the token model."""
    class Meta:
        model = Token
        fields = ('id', 'name',)


class CurrencySerializer(ModelSerializer):
    """Serializer for the currency model."""
    class Meta:
        model = Token
        fields = ('id', 'name',)


class TickerSerializer(ModelSerializer):
    """Serializer for the trading pair model."""
    token = TokenSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = TradingPair
        fields = ('id', 'token', 'currency',
                  'price_precision', 'quantity_precision',)


class GridSerializer(ModelSerializer):
    """Serializer for the grid model."""
    ticker = TickerSerializer()

    class Meta:
        model = Grid
        fields = ('id', 'top', 'bottom', 'number_of_levels',
                  'deposit', 'ticker',)


class DealSerializer(ModelSerializer):
    """Serializer for the deal model."""
    ticker = TickerSerializer()

    class Meta:
        model = Deal
        fields = ('id', 'opening_date', 'closed', 'ticker',
                  'quantity', 'purchase_price', 'selling_price',
                  'revenue', 'trader',)
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        quantity = instance.quantity
        purchase_price = instance.purchase_price
        selling_price = validated_data['selling_price']
        instance.selling_price = selling_price
        revenue = round(quantity * (selling_price - purchase_price), 2)
        instance.revenue = revenue
        instance.closed = True
        instance.save()
        return instance


class TraderSerializer(ModelSerializer):
    """Serializer for the trader model."""
    grid = GridSerializer()

    class Meta:
        model = Trader
        fields = ('id', 'creation_date', 'working', 'initial_deposit',
                  'current_deposit', 'revenue', 'market', 'exchange',
                  'grid',)
        read_only_fields = ('id',)
