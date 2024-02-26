from rest_framework.serializers import ModelSerializer

from deals.models import Deal, Trader


class DealSerializer(ModelSerializer):
    """Serializer for the deal model."""
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
    class Meta:
        model = Trader
        fields = ('id', 'creation_date', 'working', 'initial_deposit',
                  'current_deposit', 'revenue', 'market', 'ticker',
                  'exchange',)
        read_only_fields = ('id',)
