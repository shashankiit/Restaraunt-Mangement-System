# Generated by Django 3.2 on 2021-04-16 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userlog', '0005_alter_user_area_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='area_code',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]