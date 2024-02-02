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
    purchase_price = models.FloatField(
        verbose_name='Trade entry price',
    )
    selling_price = models.FloatField(
        verbose_name='Trade exit price',
        blank=True,
        null=True,
    )
    trader = models.ForeignKey(
        'Trader',
        verbose_name='Trader who made the deal',
        on_delete=models.SET_NULL,
        related_name='deals',
        null=True,
    )


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
    """
    revenue = models.GeneratedField(
        verbose_name='Revenue for trader',
        expression=
        (models.F('current_deposit') - models.F('initial_deposit')) * 100 /
        models.F('initial_deposit'),
        db_persist=False,
        output_field=models.IntegerField(),
    )
    """
    market = models.CharField(
        verbose_name='The market where the bot trades',
        max_length=20,
        choices=MARKET_CHOICES,
    )
