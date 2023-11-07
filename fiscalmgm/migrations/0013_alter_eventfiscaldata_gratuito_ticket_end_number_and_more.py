# Generated by Django 4.2 on 2023-11-06 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscalmgm', '0012_alter_eventfiscaldata_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventfiscaldata',
            name='gratuito_ticket_end_number',
            field=models.IntegerField(default=0, null=True, verbose_name='Gratuito al numero'),
        ),
        migrations.AlterField(
            model_name='eventfiscaldata',
            name='gratuito_ticket_start_number',
            field=models.IntegerField(default=0, null=True, verbose_name='Gratuito dal numero'),
        ),
        migrations.AlterField(
            model_name='eventfiscaldata',
            name='intero_ticket_end_number',
            field=models.IntegerField(default=0, null=True, verbose_name='Intero al numero'),
        ),
        migrations.AlterField(
            model_name='eventfiscaldata',
            name='intero_ticket_start_number',
            field=models.IntegerField(default=0, null=True, verbose_name='Intero dal numero'),
        ),
        migrations.AlterField(
            model_name='eventfiscaldata',
            name='ridotto_ticket_end_number',
            field=models.IntegerField(default=0, null=True, verbose_name='Ridotto al numero'),
        ),
        migrations.AlterField(
            model_name='eventfiscaldata',
            name='ridotto_ticket_start_number',
            field=models.IntegerField(default=0, null=True, verbose_name='Ridotto dal numero'),
        ),
    ]
