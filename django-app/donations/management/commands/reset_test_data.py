from django.core.management.base import BaseCommand

from newstream.test_data import reset_test_data

class Command(BaseCommand):
    help = 'Reset test data'

    def handle(self, *args, **options):
        reset_test_data()
