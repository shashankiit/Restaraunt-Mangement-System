# Generated by Django 3.2 on 2021-04-29 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takeaway', '0003_order_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_ingredient',
            name='day',
            field=models.DateField(auto_now_add=True),
        ),
    ]