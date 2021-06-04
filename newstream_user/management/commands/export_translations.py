from zipfile import ZipFile
import csv
import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from donations.models import DonationForm
from email_campaigns.models import EmailTemplate, TargetGroup, Campaign
from site_settings.models import SiteSettings
from pages.models import HomePage

class Command(BaseCommand):
    help = 'updates .po files, compiles all i18n fields into a csv file and zips them all into one zip file'

    def handle(self, *args, **options):
        ## Update .po files
        try:
            subprocess.run(["python", "manage.py", "makemessages", "-a"])
        except:
            print('error generating po files')

        # Get all the .po files
        file_paths = []
        for root, directories, files in os.walk('./'):
            for filename in files:
                if 'django.po' in filename:
                    # join the two strings in order to form the full filepath.
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)

        ## Write model fields in a csv

        donforms = DonationForm.objects.all()
        donFormsHeadings = ['title', 'description', 'donation_footer_text']

        emailTemps = EmailTemplate.objects.all()
        emailTempsHeadings = ['title', 'subject', 'plain_text', 'html_body']

        targetGroups = TargetGroup.objects.all()

        campaigns = Campaign.objects.all()

        siteSettings = SiteSettings.objects.all()
        siteSettingsHeadings = ['signup_footer_text', '_2c2p_frontend_label', 'paypal_frontend_label', 'paypal_legacy_frontend_label',
             'stripe_frontend_label', 'manual_frontend_label', 'offline_frontend_label', 'offline_instructions_text', 'offline_thankyou_text']

        homePages = HomePage.objects.all()

        with open('translation_fields.csv', 'w', newline='') as f:
            writer = csv.writer(f)

            if donforms:
                writer.writerow(['Donation Forms'])
                writer.writerow(donFormsHeadings)
                for form in donforms:
                    writer.writerow([getattr(form, field) for field in donFormsHeadings])
            
            if emailTemps:
                writer.writerow(['Email Templates'])
                writer.writerow(emailTempsHeadings)
                for email in emailTemps:
                    writer.writerow([getattr(email, field) for field in emailTempsHeadings])
            
            if targetGroups:
                writer.writerow(['Target Group'])
                writer.writerow(['title'])
                for target in targetGroups:
                    writer.writerow([getattr(target, 'title')])
            
            if campaigns:
                writer.writerow(['Campaigns'])
                writer.writerow(['title'])
                for campaign in campaigns:
                    writer.writerow([getattr(campaign, 'title')])
            
            if siteSettings:
                writer.writerow(['Site Settings'])
                writer.writerow(siteSettingsHeadings)
                for setting in siteSettings:
                    writer.writerow([getattr(setting, field) for field in siteSettingsHeadings])
            
            if homePages:
                writer.writerow(['Home Pages'])
                writer.writerow(['body'])
                for homePage in homePages:
                    writer.writerow([getattr(homePage, 'body')])
            
        # zip all the files together
        with ZipFile('translation_files.zip', 'w') as zip:
            for file in file_paths:
                zip.write(file)
            zip.write('translation_fields.csv')
        print('Zip file generated')
