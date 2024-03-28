from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        PrimaryKeyRelatedField)

from deals.models import (Deal, Trader, Grid, Level,
                          Token, Currency, Ticker)


class TokenSerializer(ModelSerializer):
    """Serializer for the token model."""
    class Meta:
        model = Token
        fields = ('id', 'name',)


class CurrencySerializer(ModelSerializer):
    """Serializer for the currency model."""
    class Meta:
        model = Currency
        fields = ('id', 'name',)


class TickerSerializer(ModelSerializer):
    """Serializer for the ticker model."""
    token = TokenSerializer()
    currency = CurrencySerializer()
    name = SerializerMethodField()

    class Meta:
        model = Ticker
        fields = ('id', 'token', 'currency',
                  'price_precision', 'quantity_precision',
                  'name')

    def get_name(self, obj):
        name = obj.token.name + obj.currency.name
        return name


class LevelSerializer(ModelSerializer):
    """Serializer for the level model."""
    grid = PrimaryKeyRelatedField(queryset=Grid.objects.all(),
                                  allow_null=True)
    deal = PrimaryKeyRelatedField(queryset=Deal.objects.all(),
                                  allow_null=True)

    class Meta:
        model = Level
        fields = ('id', 'side', 'order_id', 'price',
                  'quantity', 'inverse', 'grid', 'deal',)


class GridSerializer(ModelSerializer):
    """Serializer for the grid model."""
    ticker = TickerSerializer()
    levels = SerializerMethodField()

    class Meta:
        model = Grid
        fields = ('id', 'bottom', 'top', 'number_of_levels',
                  'deposit', 'ticker', 'installed', 'step',
                  'order_size', 'levels',)

    def get_levels(self, obj):
        levels = obj.levels.values(
            'id',
            'side',
            'order_id',
            'price',
            'quantity',
            'inverse',
            'grid',
            'deal',)
        return levels


class CreateGridSerializer(ModelSerializer):
    """Serializer to create a grid object."""
    ticker = PrimaryKeyRelatedField(queryset=Ticker.objects.all())

    class Meta:
        model = Grid
        fields = ('id', 'bottom', 'top', 'number_of_levels',
                  'deposit', 'ticker')


class DealSerializer(ModelSerializer):
    """Serializer for the deal model."""

    class Meta:
        model = Deal
        fields = ('id', 'opening_date', 'closed', 'ticker',
                  'side', 'quantity', 'entry_price', 'exit_price',
                  'revenue', 'trader',)

    def update(self, instance, validated_data):
        exit_price = validated_data['exit_price']
        instance.exit_price = exit_price
        if instance.side == 'long':
            instance.revenue = round(
                instance.quantity * (exit_price - instance.entry_price), 2)
        else:
            instance.revenue = round(
                instance.quantity * (instance.entry_price - exit_price), 2)
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
                  'grid', 'lock',)
        read_only_fields = ('id',)
