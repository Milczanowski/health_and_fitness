# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-14 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0020_remove_meal_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='Time',
            field=models.IntegerField(default=0),
        ),
    ]