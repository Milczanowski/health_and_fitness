# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-13 12:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0005_diets_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodingredient',
            name='Creation_Data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
