from django.db import models


class Deal(models.Model):
    """Model for deals."""
    STATUS_CHOICES = (
        ('C', 'Closed'),
        ('P', 'In progress'),
    )
    id = models.AutoField(primary_key=True)
    opening_date = models.DateField(
        verbose_name='Trade opening date',
        auto_now_add=True,
    )
    status = models.CharField(
        verbose_name='Status of deal',
        choices=STATUS_CHOICES,
    )
    purchase_price = models.FloatField(
        verbose_name='Trade entry price',
    )
    selling_price = models.FloatField(
        verbose_name='Trade exit price',
        blank=True,
    )
