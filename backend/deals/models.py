from django.db import models


class Deal(models.Model):
    """Model for deals."""
    id = models.AutoField(primary_key=True)
    opening_date = models.DateField(
        verbose_name='Trade opening date',
        auto_now_add=True,
    )
    closed = models.BooleanField(
        verbose_name='Status of deal',
        default=False,
    )
    ticker = models.CharField(
        verbose_name='Coin ticker',
        max_length=20,
    )
    quantity = models.FloatField(
        verbose_name='Quantity purchased',
    )
    purchase_price = models.FloatField(
        verbose_name='Trade entry price',
    )
    selling_price = models.FloatField(
        verbose_name='Trade exit price',
        blank=True,
        null=True,
        default=None,
    )
    revenue = models.FloatField(
        verbose_name='Revenue for deal',
        blank=True,
        null=True,
        default=None,
    )
    trader = models.ForeignKey(
        'Trader',
        verbose_name='Trader who made the deal',
        on_delete=models.SET_NULL,
        related_name='deals',
        null=True,
    )

    class Meta:
        ordering = ('-id',)


class Trader(models.Model):
    """Model for trading bots."""
    MARKET_CHOICES = (
        ('S', 'Spot'),
        ('F', 'Futures'),
    )
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(
        verbose_name='Trading bot creation date',
        auto_now_add=True,
    )
    working = models.BooleanField(
        verbose_name='Status of trading bot',
        default=False,
    )
    initial_deposit = models.FloatField(
        verbose_name='Trading bot starting deposit',
    )
    current_deposit = models.FloatField(
        verbose_name='Trading bot current deposit',
        blank=True,
        null=True,
    )
    revenue = models.GeneratedField(
        verbose_name='Revenue for trading bot',
        expression=models.F('current_deposit') - models.F('initial_deposit'),
        db_persist=True,  # True для postgres
        output_field=models.FloatField(),
    )
    market = models.CharField(
        verbose_name='The market where the bot trades',
        max_length=20,
        choices=MARKET_CHOICES,
        default='S',
    )
    token = models.CharField(
        verbose_name='Name of the coin being traded.',
        max_length=7,
    )
    currency = models.CharField(
        verbose_name='Stablecoin of the traded pair.',
        max_length=7,
    )
    exchange = models.CharField(
        verbose_name='Exchange for trading.',
        max_length=20,
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.id
