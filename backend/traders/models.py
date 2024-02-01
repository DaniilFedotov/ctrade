from django.db import models


class Trader(models.Model):
    """Model for trading bots."""
    STATUS_CHOICES = (
        ('O', 'Off'),
        ('W', 'In working'),
    )
    MARKET_CHOICES = (
        ('S', 'Spot'),
        ('F', 'Futures'),
    )
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(
        verbose_name='Trading bot creation date',
        auto_now_add=True,
    )
    status = models.CharField(
        verbose_name='Status of trading bot',
        choices=STATUS_CHOICES,
    )
    initial_deposit = models.FloatField(
        verbose_name='Trading bot starting deposit',
    )
    current_deposit = models.FloatField(
        verbose_name='Trading bot current deposit',
        blank=True,
    )
    market = models.CharField(
        verbose_name='The market where the bot trades',
        choices=MARKET_CHOICES,
    )
