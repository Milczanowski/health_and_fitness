# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-13 22:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0009_auto_20170213_2318'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dish',
            new_name='Meal',
        ),
        migrations.RenameField(
            model_name='diets',
            old_name='Dishs',
            new_name='Meals',
        ),
    ]
