from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Deal(models.Model):
    """Model for deals."""
    id = models.AutoField(
        primary_key=True,
    )
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
    id = models.AutoField(
        primary_key=True,
    )
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
    token = models.ForeignKey(
        'Token',
        verbose_name='Name of the coin being traded.',
        on_delete=models.SET_NULL,
        related_name='traders',
    )
    currency = models.ForeignKey(
        'Currency',
        verbose_name='Stablecoin of the traded pair.',
        on_delete=models.SET_NULL,
        related_name='traders',
    )
    exchange = models.CharField(
        verbose_name='Exchange for trading.',
        max_length=20,
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.id


class Grid(models.Model):
    """Model for grid description."""
    id = models.AutoField(
        primary_key=True,
    )
    top = models.FloatField(
        verbose_name='Grid top border.'
    )
    bottom = models.FloatField(
        verbose_name='Grid bottom border.'
    )
    number_of_levels = models.PositiveIntegerField(
        verbose_name='Number of grid levels.',
        validators=[
            MaxValueValidator(20),
            MinValueValidator(6),]
    )
    deposit = models.FloatField(
        verbose_name='Deposit for strategy.'
    )
    token = models.ForeignKey(
        'Token',
        verbose_name='Name of the coin being traded.',
        on_delete=models.SET_NULL,
        related_name='grids',
    )
    currency = models.ForeignKey(
        'Currency',
        verbose_name='Stablecoin of the traded pair.',
        on_delete=models.SET_NULL,
        related_name='grids',
    )


class Token(models.Model):
    """Model for token."""
    id = models.AutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=10,
    )

    def __str__(self):
        return self.name


class Currency(models.Model):
    """Model for a currency such as stablecoin."""
    id = models.AutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=10,
    )

    def __str__(self):
        return self.name


class TokenCurrency(models.Model):
    """Model for are trading pair."""
    token = models.ForeignKey(
        'Token',
        verbose_name='Linked model for a token.',
        on_delete=models.CASCADE,
    )
    currency = models.ForeignKey(
        'Currency',
        verbose_name='Linked model for a currency.',
        on_delete=models.CASCADE,
    )
    precision = models.FloatField(
        verbose_name='Price precision for a trading pair.'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['token', 'currency'],
                name='tokencurrency_unique')]
