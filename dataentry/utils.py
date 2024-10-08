import datetime
import hashlib
import time
import os
from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings

from emails.models import Email, Sent, EmailTracking, Subscriber
from bs4 import BeautifulSoup

def get_all_custom_models():
    default_models = ['ContentType', 'Session', 'LogEntry', 'Group', 'Permission', 'User', 'Upload']
    # Try to get all the apps
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
        raise CommandError(f"Model '{model_name}' not found in any app")

    # Get all the field names of the model we found
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            # Compare CSV header with model's field names
            if csv_header != model_fields:
                raise DataError(f'CSV file does not match with the {model_name} table fields')
    except Exception as e:
        raise e

    # Notify the user by email
    return model

def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL

        for recipient_email in to_email:
            # Create email tracking record
            new_message = message
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email=email,
                    subscriber=subscriber,
                    unique_id=unique_id,
                )

                base_url = settings.BASE_URL
            # Generate the tracking pixel url
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"

            # Search for the links in the email body
                soup = BeautifulSoup(message, 'html.parser')
                urls = [a['href'] for a in soup.find_all('a', href=True)]
            # If there are any links or urls in the email body, inject or clock tracking url to the original link
                if urls:
                    new_message = message
                    for url in urls:
                        # make the final tracking url
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f"{url}", f"{tracking_url}")
                else:
                    new_message = message
                    print('No URLS found in the email content')

                # Create email content with the tracking pixel image
                open_tracking_img = f"<img src='{open_tracking_url}' width='1' height='1'>"
                new_message += open_tracking_img

            # Create email message
            mail = EmailMessage(
                mail_subject,
                new_message,
                from_email,
                to=[recipient_email]
            )

            # Attach files if provided
            if attachment is not None:
                mail.attach_file(attachment)

            # Set the content subtype to HTML
            mail.content_subtype = "html"
            mail.send()

        # Store the total sent emails inside the Sent model
        if email:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()

    except Exception as e:
        raise e

def generate_csv_file(model_name):
    # Generate the timestamp of the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Define the CSV file name/path
    export_dir = 'exported_files'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    print('file_path==>', file_path)
    return file_path
