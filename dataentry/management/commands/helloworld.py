from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Prints "HelloWorld" to the console'

    def handle(self, *args, **kwargs):
        self.stdout.write('HelloWorld')
