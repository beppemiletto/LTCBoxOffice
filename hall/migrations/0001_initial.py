# Generated by Django 4.2 on 2023-04-23 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3, unique=True)),
                ('row', models.CharField(max_length=1)),
                ('num_in_row', models.CharField(max_length=1)),
                ('number', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
