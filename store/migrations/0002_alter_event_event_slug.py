# Generated by Django 4.2 on 2023-04-23 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_slug',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
