import csv

from django.core.management.base import BaseCommand

from deals.models import Deal, Trader

PATH = 'static/data/'
FILES__MODELS = {
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
                        'Предыдущие данные удалены.'))
                model.objects.bulk_create(records)
                self.stdout.write(self.style.SUCCESS('Данные импортированы.'))
                csvfile.close()
