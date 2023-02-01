from django.core.management.base import BaseCommand

from newstream.test_data import load_test_data

class Command(BaseCommand):
    help = 'Load test data'

    def handle(self, *args, **options):
        load_test_data()
