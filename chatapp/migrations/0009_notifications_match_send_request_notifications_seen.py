# Generated by Django 5.0.6 on 2024-07-07 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0008_remove_notifications_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='match_send_request',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notifications',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
