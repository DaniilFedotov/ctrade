# Generated by Django 5.0 on 2024-02-02 12:39

import django.db.models.deletion
import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trader',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Trading bot creation date')),
                ('status', models.CharField(choices=[('O', 'Off'), ('W', 'In working')], max_length=20, verbose_name='Status of trading bot')),
                ('initial_deposit', models.FloatField(verbose_name='Trading bot starting deposit')),
                ('current_deposit', models.FloatField(blank=True, verbose_name='Trading bot current deposit')),
                ('revenue', models.GeneratedField(db_persist=False, expression=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('current_deposit'), '-', models.F('initial_deposit')), '*', models.Value(100)), '/', models.F('initial_deposit')), output_field=models.FloatField(), verbose_name='Revenue for trader')),
                ('market', models.CharField(choices=[('S', 'Spot'), ('F', 'Futures')], max_length=20, verbose_name='The market where the bot trades')),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('opening_date', models.DateField(auto_now_add=True, verbose_name='Trade opening date')),
                ('status', models.CharField(choices=[('C', 'Closed'), ('P', 'In progress')], max_length=20, verbose_name='Status of deal')),
                ('ticker', models.CharField(max_length=20, verbose_name='Coin ticker')),
                ('purchase_price', models.FloatField(verbose_name='Trade entry price')),
                ('selling_price', models.FloatField(blank=True, verbose_name='Trade exit price')),
                ('trader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deals', to='deals.trader', verbose_name='Trader who made the deal')),
            ],
        ),
    ]
