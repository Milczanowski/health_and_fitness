# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-14 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0018_auto_20170214_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='Difficulty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='meal',
            name='Time',
            field=models.IntegerField(default=0),
        ),
    ]
