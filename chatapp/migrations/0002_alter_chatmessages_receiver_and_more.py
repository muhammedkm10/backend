# Generated by Django 5.0.6 on 2024-06-24 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessages',
            name='receiver',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='chatmessages',
            name='sender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
