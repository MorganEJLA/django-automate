from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Greets the user"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Indicates the name of the user")
    def handle(self, *args, **kwargs):
        #Write the logic
        name = kwargs["name"]
        greetings = f"Hello, {name}, Good Morning!"
        self.stdout.write(self.style.SUCCESS(greetings))
