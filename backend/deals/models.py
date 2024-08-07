from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Deal(models.Model):
    """Model for deals."""
    id = models.AutoField(
        primary_key=True
    )
    opening_date = models.DateField(
        verbose_name="Trade opening date",
        auto_now_add=True
    )
    closed = models.BooleanField(
        verbose_name="Status of deal",
        default=False
    )
    ticker = models.ForeignKey(
        "Ticker",
        verbose_name="Ticker of the coin being traded",
        on_delete=models.SET_NULL,
        null=True
    )
    side = models.CharField(
        verbose_name="Deal type",
        max_length=5
    )
    quantity = models.FloatField(
        verbose_name="Quantity purchased"
    )
    entry_price = models.FloatField(
        verbose_name="Trade entry price"
    )
    exit_price = models.FloatField(
        verbose_name="Trade exit price",
        blank=True,
        null=True,
        default=None
    )
    revenue = models.FloatField(
        verbose_name="Revenue for deal",
        blank=True,
        null=True,
        default=None
    )
    trader = models.ForeignKey(
        "Trader",
        verbose_name="Trader who made the deal",
        on_delete=models.SET_NULL,
        related_name="deals",
        null=True
    )

    class Meta:
        ordering = ("-id",)


class Trader(models.Model):
    """Model for trading bots."""
    MARKET_CHOICES = (
        ("S", "Spot"),
        ("F", "Futures")
    )
    id = models.AutoField(
        primary_key=True
    )
    creation_date = models.DateField(
        verbose_name="Trading bot creation date",
        auto_now_add=True
    )
    working = models.BooleanField(
        verbose_name="Status of trading bot",
        default=False
    )
    initial_deposit = models.FloatField(
        verbose_name="Trading bot starting deposit",
        blank=True,
        null=True,
        default=None
    )
    current_deposit = models.FloatField(
        verbose_name="Trading bot current deposit",
        blank=True,
        null=True,
        default=None
    )
    revenue = models.GeneratedField(
        verbose_name="Revenue for trading bot",
        expression=models.F("current_deposit") - models.F("initial_deposit"),
        db_persist=True,  # True для postgres
        output_field=models.FloatField()
    )
    market = models.CharField(
        verbose_name="The market where the bot trades",
        max_length=20,
        choices=MARKET_CHOICES,
        default="S"
    )
    exchange = models.CharField(
        verbose_name="Exchange for trading",
        max_length=20
    )
    grid = models.ForeignKey(
        "Grid",
        verbose_name="Grid settings for trading",
        on_delete=models.CASCADE
    )
    lock = models.FloatField(
        verbose_name="Amount of locked assets",
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.id


class Grid(models.Model):
    """Model for grid description."""
    id = models.AutoField(
        primary_key=True
    )
    bottom = models.FloatField(
        verbose_name="Grid bottom border"
    )
    top = models.FloatField(
        verbose_name="Grid top border"
    )
    number_of_levels = models.PositiveIntegerField(
        verbose_name="Number of grid levels",
        validators=[
            MaxValueValidator(40),
            MinValueValidator(6)]
    )
    deposit = models.FloatField(
        verbose_name="Deposit for strategy"
    )
    ticker = models.ForeignKey(
        "Ticker",
        verbose_name="Ticker of the coin being traded",
        on_delete=models.CASCADE
    )
    installed = models.BooleanField(
        verbose_name="Status of grid",
        default=False
    )
    step = models.FloatField(
        verbose_name="Grid step",
        blank=True,
        null=True,
        default=None
    )
    order_size = models.FloatField(
        verbose_name="Amount of currency per order",
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        ordering = ("-id",)


class Level(models.Model):
    """Model for a level array."""
    SIDE_CHOICES = (
        ("buy", "Buy order"),
        ("sell", "Sell order")
    )
    id = models.AutoField(
        primary_key=True
    )
    side = models.CharField(
        verbose_name="Order type",
        max_length=4,
        choices=SIDE_CHOICES
    )
    order_id = models.CharField(
        verbose_name="Exchange order id",
        max_length=20,
        blank=True,
        null=True,
        default=None
    )
    price = models.FloatField(
        verbose_name="Order price"
    )
    quantity = models.FloatField(
        verbose_name="Number of coins in the order"
    )
    inverse = models.BooleanField(
        verbose_name="Indicates an order that goes beyond the original grid",
        default=False
    )
    grid = models.ForeignKey(
        "Grid",
        verbose_name="Grid-parent",
        on_delete=models.CASCADE,
        related_name="levels"
    )
    deal = models.ForeignKey(
        "Deal",
        verbose_name="Related deal",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None
    )


class Token(models.Model):
    """Model for token."""
    id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.name


class Currency(models.Model):
    """Model for a currency such as stablecoin."""
    id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.name


class Ticker(models.Model):
    """Model for are trading pair."""
    id = models.AutoField(
        primary_key=True
    )
    token = models.ForeignKey(
        "Token",
        verbose_name="Linked model for a token",
        on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        "Currency",
        verbose_name="Linked model for a currency",
        on_delete=models.CASCADE
    )
    price_precision = models.IntegerField(
        verbose_name="Price precision for a trading pair in decimal places"
    )
    quantity_precision = models.IntegerField(
        verbose_name="Quantity precision for a trading pair in decimal places"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["token", "currency"],
                name="tradingpair_unique")]

    def __str__(self):
        return self.token.name + self.currency.name
