# Generated by Django 4.0.1 on 2022-03-22 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growthmodel', '0004_rename_status_growthmodelactivity_activity_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profession',
        ),
    ]
