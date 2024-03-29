# Generated by Django 3.0.8 on 2020-08-14 14:17

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('from_address', models.EmailField(max_length=254)),
                ('sent', models.BooleanField(default=False, editable=False)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Campaign',
                'verbose_name_plural': 'Campaigns',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('plain_text', models.TextField()),
                ('html_body', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Email Template',
                'verbose_name_plural': 'Email Templates',
            },
        ),
        migrations.CreateModel(
            name='TargetGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Target Group',
                'verbose_name_plural': 'Target Groups',
            },
        ),
    ]
