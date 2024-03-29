# Generated by Django 3.1.11 on 2023-04-20 09:50

import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    def drop_index_if_exists(apps, schema_editor):
        schema_editor.execute('DROP INDEX IF EXISTS "donations_subscription_created_by_id_51971c35";')
        schema_editor.execute('DROP INDEX IF EXISTS "donations_subscription_user_id_f379235d";')

    dependencies = [
        ('site_settings', '0032_sitesettings_default_from_name'),
        ('newstream_user', '0012_auto_20210601_0929'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donations', '0038_donationform_max_amount'),
    ]

    operations = [
        # This is needed as renaming model in django doesn't drop old indexes in Pgsql
        migrations.RunPython(drop_index_if_exists),
        migrations.RenameModel(
            old_name='Subscription',
            new_name='SubscriptionInstance',
        ),
        migrations.AlterField(
            model_name='subscriptioninstance',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscription_instance_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subscription_created_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscription_created_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subscriptioninstance',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscription_instances', to='donations.subscription'),
        ),
    ]
