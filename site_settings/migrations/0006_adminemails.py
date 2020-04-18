# Generated by Django 3.0.5 on 2020-04-17 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0005_auto_20200414_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminEmails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('setting_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_emails', to='site_settings.GlobalSettings')),
            ],
        ),
    ]