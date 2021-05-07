# Generated by Django 3.2 on 2021-05-06 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dining_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_id', models.IntegerField(unique=True)),
                ('capacity', models.IntegerField()),
                ('phone_occupied', models.BigIntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_id', models.IntegerField()),
                ('phone', models.BigIntegerField(default=None)),
                ('date_for_res', models.DateField()),
                ('num_diners', models.IntegerField()),
                ('time_for_res', models.TimeField()),
                ('reservation_duration', models.TimeField()),
            ],
        ),
    ]
