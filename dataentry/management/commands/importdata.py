from django.core.management.base import BaseCommand, CommandError
import csv
# from dataentry.models import Student
from django.apps import apps


class Command(BaseCommand):
    help = 'It will import data into the database from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Indicates the file path')
        parser.add_argument('model_name', type=str, help='Indicates the model name')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue

        if not model:
            raise CommandError(f"Model '{model_name}' is found in any app")

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
