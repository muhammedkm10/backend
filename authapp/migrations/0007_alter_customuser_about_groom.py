# Generated by Django 5.0.6 on 2024-06-02 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='about_groom',
            field=models.TextField(blank=True, null=True),
        ),
    ]
