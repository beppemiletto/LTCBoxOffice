# Generated by Django 4.2 on 2023-05-03 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_event_event_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sold_out',
            field=models.BooleanField(default=False),
        ),
    ]
