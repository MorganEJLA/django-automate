from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
from django.db import DataError

from dataentry.utils import check_csv_errors
# from dataentry.models import Student


class Command(BaseCommand):
    help = 'It will import data into the database from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Indicates the file path')
        parser.add_argument('model_name', type=str, help='Indicates the model name')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        model = check_csv_errors(file_path, model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
