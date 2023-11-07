# Generated by Django 4.2 on 2023-11-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscalmgm', '0014_eventfiscaldata_printed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventfiscaldata',
            old_name='gratuito_ticket_end_number',
            new_name='gratuito_ticket_end_number_1',
        ),
        migrations.RenameField(
            model_name='eventfiscaldata',
            old_name='gratuito_ticket_serie',
            new_name='gratuito_ticket_serie_1',
        ),
        migrations.RenameField(
            model_name='eventfiscaldata',
            old_name='intero_ticket_serie',
            new_name='gratuito_ticket_serie_2',
        ),
        migrations.RenameField(
            model_name='eventfiscaldata',
            old_name='gratuito_ticket_start_number',
            new_name='gratuito_ticket_start_number_1',
        ),
        migrations.RenameField(
            model_name='eventfiscaldata',
            old_name='intero_ticket_end_number',
            new_name='intero_ticket_end_number_1',
        ),
        migrations.RenameField(
            model_name='eventfiscaldata',
            old_name='ridotto_ticket_serie',
            new_name='intero_ticket_serie_1',
        ),
        migrations.RenameField(
            model_name='eventfiscaldata',
            old_name='intero_ticket_start_number',
            new_name='intero_ticket_start_number_1',
        ),
        migrations.RenameField(
            model_name='eventfiscaldata',
            old_name='ridotto_ticket_end_number',
            new_name='ridotto_ticket_end_number_1',
        ),
        migrations.RenameField(
            model_name='eventfiscaldata',
            old_name='ridotto_ticket_start_number',
            new_name='ridotto_ticket_start_number_1',
        ),
        migrations.AddField(
            model_name='eventfiscaldata',
            name='gratuito_ticket_end_number_2',
            field=models.IntegerField(default=0, null=True, verbose_name='Gratuito al numero'),
        ),
        migrations.AddField(
            model_name='eventfiscaldata',
            name='gratuito_ticket_start_number_2',
            field=models.IntegerField(default=0, null=True, verbose_name='Gratuito dal numero'),
        ),
        migrations.AddField(
            model_name='eventfiscaldata',
            name='intero_ticket_end_number_2',
            field=models.IntegerField(default=0, null=True, verbose_name='Intero al numero'),
        ),
        migrations.AddField(
            model_name='eventfiscaldata',
            name='intero_ticket_serie_2',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='eventfiscaldata',
            name='intero_ticket_start_number_2',
            field=models.IntegerField(default=0, null=True, verbose_name='Intero dal numero'),
        ),
        migrations.AddField(
            model_name='eventfiscaldata',
            name='ridotto_ticket_end_number_2',
            field=models.IntegerField(default=0, null=True, verbose_name='Ridotto al numero'),
        ),
        migrations.AddField(
            model_name='eventfiscaldata',
            name='ridotto_ticket_serie_1',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='eventfiscaldata',
            name='ridotto_ticket_serie_2',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='eventfiscaldata',
            name='ridotto_ticket_start_number_2',
            field=models.IntegerField(default=0, null=True, verbose_name='Ridotto dal numero'),
        ),
    ]
