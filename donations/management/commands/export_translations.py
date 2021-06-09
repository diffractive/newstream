import csv
import os
import re
from zipfile import ZipFile
from django.core.management.base import BaseCommand
from django.apps import apps

from pages.models import HomePage

class Command(BaseCommand):
    help = 'updates .po files, compiles all i18n fields into a csv file and zips them all into one zip file'

    def handle(self, *args, **options):
        # Get all i18nfields values from all models + page content
        with open('translation_fields.csv', 'w', newline='') as f:
            writer = csv.writer(f)

            # header
            writer.writerow(['Field/Model Name', 'Field Value'])

            for model in apps.get_models():
                i18n_fields = []
                for field in model._meta.get_fields():
                    # relational fields cannot be deconstructed, we don't have translated relational fields anyway
                    if hasattr(field, 'deconstruct'):
                        # more on deconstruct: https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.Field.deconstruct
                        field_info = field.deconstruct()
                        field_name = field_info[0]
                        import_path = field_info[1]
                        if re.search(r'(I18nCharField|I18nTextField|I18nRichTextField)$', import_path):
                            i18n_fields.append(field_name)
                # loop over all instances to get all english values from the i18n_fields
                if len(i18n_fields):
                    # First make a row for this model
                    writer.writerow(['[Model] %s' % model.__name__])
                    for obj in model.objects.all():
                        for field in i18n_fields:
                            writer.writerow(['[Field] #%i - %s' % (obj.id, field), getattr(obj, field).localize('en')])

            # loop over all pages (HomePage)
            writer.writerow(['[Model] %s' % 'HomePage'])
            for page in HomePage.objects.all():
                # the locale field might still hasn't been set yet if the page wasn't saved after the locales are introduced
                if str(page.locale) == 'English' or not page.locale:
                    writer.writerow(['[Field] #%i - %s' % (page.id, 'body'), page.body])
            

        # Get all the .po files
        file_paths = []
        for root, directories, files in os.walk('./'):
            if not re.search(r'^\./(venv|virtualenv|node_modules|\.git)', root):
                for filename in files:
                    if 'django.po' in filename:
                        # join the two strings in order to form the full filepath.
                        filepath = os.path.join(root, filename)
                        file_paths.append(filepath)

        # zip all the files together
        with ZipFile('translation_files.zip', 'w') as zip:
            for file in file_paths:
                zip.write(file)
            zip.write('translation_fields.csv')
        print('Zip file generated')