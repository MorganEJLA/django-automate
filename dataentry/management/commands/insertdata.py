from django.core.management.base import BaseCommand
from dataentry.models import Student
#I want to add some data to the database using the custom command

class Command(BaseCommand):
    help = 'Inserts data into the database'

    def handle(self, *args, **kwargs):
        dataset = [
            {'roll_no': 1002, 'name': 'John', 'age': 22},
            {'roll_no': 1003, 'name': 'Doe', 'age': 23},
            {'roll_no': 1004, 'name': 'Mike', 'age': 24},
            {'roll_no': 1005, 'name': 'Jane', 'age': 25},
            {'roll_no': 1006, 'name': 'Dane', 'age': 26},
        ]
        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()
            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'],name=data['name'], age=data['age'])
            else:
                self.stdout.write(self.style.WARNING(f'Student with roll number {roll_no} already exists in the database. Skipping...'))
        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))
