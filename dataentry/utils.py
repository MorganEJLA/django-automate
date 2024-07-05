from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError

def get_all_custom_models():
    default_models = ['ContentType', 'Session', 'LogEntry', 'Group', 'Permission', 'User', 'Upload']
    #try to get all the apps
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)

    return custom_models

def check_csv_errors(file_path, model_name):
     model = None
     for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue

     if not model:
        raise CommandError(f"Model '{model_name}' is found in any app")

    #get all the field names of the model we found
     model_fields = [field.name for field in model._meta.fields if field.name != 'id']

     try:
      with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        csv_header = reader.fieldnames

        #compare csv header with model's field names
        if csv_header !=model_fields:
            raise DataError(f'CSV file does not match with the {model_name} table fields')
     except Exception as e:
        raise e
    # notify the user by email
     return model
