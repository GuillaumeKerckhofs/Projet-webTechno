# Generated by Django 3.2 on 2022-05-23 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220523_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
    ]
