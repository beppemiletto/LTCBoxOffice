# Generated by Django 4.2 on 2024-01-31 17:21

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_payment_payer_given_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderevent',
            name='barcode_path',
            field=models.FilePathField(blank=True, null=True, path=orders.models.barcode_image_path),
        ),
    ]
