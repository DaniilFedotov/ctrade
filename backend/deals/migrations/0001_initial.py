# Generated by Django 5.0 on 2024-02-26 08:35

import django.core.validators
import django.db.models.deletion
import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('top', models.FloatField(verbose_name='Grid top border.')),
                ('bottom', models.FloatField(verbose_name='Grid bottom border.')),
                ('number_of_levels', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(6)], verbose_name='Number of grid levels.')),
                ('deposit', models.FloatField(verbose_name='Deposit for strategy.')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grids', to='deals.currency', verbose_name='Stablecoin of the traded pair.')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grids', to='deals.token', verbose_name='Name of the coin being traded.')),
            ],
        ),
        migrations.CreateModel(
            name='TokenCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precision', models.FloatField(verbose_name='Price precision for a trading pair.')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deals.currency', verbose_name='Linked model for a currency.')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deals.token', verbose_name='Linked model for a token.')),
            ],
        ),
        migrations.CreateModel(
            name='Trader',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Trading bot creation date')),
                ('working', models.BooleanField(default=False, verbose_name='Status of trading bot')),
                ('initial_deposit', models.FloatField(verbose_name='Trading bot starting deposit')),
                ('current_deposit', models.FloatField(blank=True, null=True, verbose_name='Trading bot current deposit')),
                ('revenue', models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(models.F('current_deposit'), '-', models.F('initial_deposit')), output_field=models.FloatField(), verbose_name='Revenue for trading bot')),
                ('market', models.CharField(choices=[('S', 'Spot'), ('F', 'Futures')], default='S', max_length=20, verbose_name='The market where the bot trades')),
                ('exchange', models.CharField(max_length=20, verbose_name='Exchange for trading.')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traders', to='deals.currency', verbose_name='Stablecoin of the traded pair.')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traders', to='deals.token', verbose_name='Name of the coin being traded.')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('opening_date', models.DateField(auto_now_add=True, verbose_name='Trade opening date')),
                ('closed', models.BooleanField(default=False, verbose_name='Status of deal')),
                ('ticker', models.CharField(max_length=20, verbose_name='Coin ticker')),
                ('quantity', models.FloatField(verbose_name='Quantity purchased')),
                ('purchase_price', models.FloatField(verbose_name='Trade entry price')),
                ('selling_price', models.FloatField(blank=True, default=None, null=True, verbose_name='Trade exit price')),
                ('revenue', models.FloatField(blank=True, default=None, null=True, verbose_name='Revenue for deal')),
                ('trader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deals', to='deals.trader', verbose_name='Trader who made the deal')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AddConstraint(
            model_name='tokencurrency',
            constraint=models.UniqueConstraint(fields=('token', 'currency'), name='tokencurrency_unique'),
        ),
    ]
