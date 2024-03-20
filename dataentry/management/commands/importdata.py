from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
from django.db import DataError
# from dataentry.models import Student


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
        #compare csv header with model fields
        #fetch all model field names

        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        print(model_fields)
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            #compare csv header with model's field names
            if csv_header !=model_fields:
                raise DataError(f'CSV file does not match with the {model_name} table fields')
            for row in reader:
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
