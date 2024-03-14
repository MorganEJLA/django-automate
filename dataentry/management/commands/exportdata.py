import csv

from django.core.management.base import BaseCommand
from django.apps import apps
from datetime import datetime

#proposed command = python manage.py exportdata model_name

class Command(BaseCommand):
    help = 'Export data from database to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Indicates the model name')

    def handle(self, *args, **kwargs):
        # fetch the data from the database
        model_name = kwargs['model_name'].capitalize()
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                pass
        if not model:
            self.stderr.write(f'Model {model_name} could not found')
            return
        #fetch the data from the database
        data = model.objects.all()
        #generate the timestamp of the current data and time
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        #define the csv file name/path
        file_path = f'exported_{model_name}_data_{timestamp}.csv'

        #open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            #write the CSV header
            writer.writerow([field.name for field in model._meta.fields])
            #fetch the data from the database
            #write data rows
            for dt in data:
                writer.writerow([getattr(dt,field.name)for field in model._meta.fields])
        self.stdout.write(self.style.SUCCESS(f'Data exported successfully'))
