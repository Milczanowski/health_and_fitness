# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-14 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0021_meal_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='c_ratting',
            field=models.FloatField(default=0),
        ),
    ]
