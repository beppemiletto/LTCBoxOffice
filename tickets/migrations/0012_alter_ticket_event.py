# Generated by Django 4.2 on 2024-06-03 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0011_alter_ticket_pdf_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='event',
            field=models.CharField(blank=True, default='', max_length=25, null=True),
        ),
    ]
