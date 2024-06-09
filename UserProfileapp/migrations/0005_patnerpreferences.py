# Generated by Django 5.0.6 on 2024-05-29 14:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfileapp', '0004_familydetails_about_family_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatnerPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patner_age', models.IntegerField(blank=True, null=True)),
                ('height', models.CharField(blank=True, max_length=50, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_toungue', models.CharField(blank=True, max_length=50, null=True)),
                ('physical_status', models.CharField(blank=True, max_length=30, null=True)),
                ('eating_habits', models.CharField(blank=True, max_length=30, null=True)),
                ('drinking_habits', models.CharField(blank=True, max_length=30, null=True)),
                ('smalking_habits', models.CharField(blank=True, max_length=30, null=True)),
                ('religion', models.CharField(blank=True, max_length=30, null=True)),
                ('cast', models.CharField(blank=True, max_length=30, null=True)),
                ('highest_education', models.CharField(blank=True, max_length=50, null=True)),
                ('employed_in', models.CharField(blank=True, max_length=30, null=True)),
                ('annual_income', models.CharField(blank=True, max_length=30, null=True)),
                ('about_partner', models.TextField(blank=True, null=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]