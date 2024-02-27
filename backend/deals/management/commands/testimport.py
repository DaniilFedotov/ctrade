import csv

from django.core.management.base import BaseCommand

from deals.models import (Deal, Trader, Grid,
                          Token, Currency, TradingPair)

PATH = 'static/data/'
FILES__MODELS = {
    'tokens': Token,
    'currencies': Currency,
    'tradingpairs': TradingPair,
    'grids': Grid,
    'traders': Trader,
    'deals': Deal,
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=False,
        )

    def handle(self, *args, **options):
        for file, model in FILES__MODELS.items():
            with open(PATH + f'{file}.csv', 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                records = []
                for row in reader:
                    records.append(model(**row))
                if options['delete_existing']:
                    model.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(
                        'Previous data deleted.'))
                model.objects.bulk_create(records)
                self.stdout.write(self.style.SUCCESS(f'Data from {file}.scv imported.'))
                csvfile.close()
