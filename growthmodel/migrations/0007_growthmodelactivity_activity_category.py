# Generated by Django 4.0.1 on 2022-03-31 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growthmodel', '0006_rename_growthmodel_id_growthmodelactivity_growth_model_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='growthmodelactivity',
            name='activity_category',
            field=models.CharField(choices=[('course', 'Course'), ('post', 'Post'), ('blog', 'Blog'), ('room', 'Room')], db_column='activityCategory', default='course', max_length=255),
        ),
    ]
