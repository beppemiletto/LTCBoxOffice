# Generated by Django 4.2 on 2023-10-27 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscalmgm', '0004_report_progres_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingresso',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
