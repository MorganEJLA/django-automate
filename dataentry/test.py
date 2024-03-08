from django.test import TestCase
from django.core.management import call_command
import io
# Create your tests here.
class CommandTestCase(TestCase):
    def test_command_output(self):
        """
        Test that the command prints the expected output
        """
        out = io.StringIO()
        call_command("Command", stdout=out)
        output = out.getvalue().strip()
        self.assertEqual(output, "Hello World")
