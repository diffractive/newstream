from django.db import migrations

def create_subscriptions_for_instances(apps, schema_editor):
    """ With the Subscription remodelling in place
        we should create a Subscription for each existing SubscriptionInstance
    """
    SubscriptionInstance = apps.get_model('donations', 'SubscriptionInstance')
    Subscription = apps.get_model('donations', 'Subscription')

    existing_instances = SubscriptionInstance.objects.all()
    for instance in existing_instances:
        subscription = Subscription(
            user=instance.user,
            subscription_created_at=instance.created_at,
            created_by=instance.created_by,
            deleted=instance.deleted
        )
        subscription.save()


def remove_subscriptions(apps, schema_editor):
    """ For reversing this migration, removing all created Subscriptions(parents of the instances)
    """
    Subscription = apps.get_model('donations', 'Subscription')
    Subscription.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0039_remodel_subscriptions'),
    ]

    operations = [
        migrations.RunPython(create_subscriptions_for_instances, remove_subscriptions),
    ]