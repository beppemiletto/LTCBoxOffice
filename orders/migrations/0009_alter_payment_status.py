# Generated by Django 4.2 on 2024-01-30 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_orderevent_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('BOOKED', 'BOOKED'), ('COMPLETED', 'COMPLETED'), ('CANCELED', 'CANCELED')], default='NEW', max_length=100),
        ),
    ]
