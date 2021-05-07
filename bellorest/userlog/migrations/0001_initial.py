# Generated by Django 3.2 on 2021-05-06 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('spent', models.IntegerField(default=0, help_text='Money spent on ingredients')),
                ('earned', models.IntegerField(default=0, help_text='Money earned from sale')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery_staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('area_code', models.IntegerField(blank=True, default=None, null=True)),
                ('available_stat', models.IntegerField(choices=[(0, 0), (1, 1)])),
                ('phone', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Loyalty_level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loyalty_points', models.IntegerField(unique=True)),
                ('discount_perc', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.BigIntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True, default=None)),
                ('area_code', models.IntegerField(blank=True, default=None, null=True)),
                ('mon_spent', models.IntegerField()),
                ('loyalty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userlog.loyalty_level')),
            ],
        ),
    ]
