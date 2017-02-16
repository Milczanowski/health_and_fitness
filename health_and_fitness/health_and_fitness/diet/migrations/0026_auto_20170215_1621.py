# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-15 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0025_remove_ingredient_voters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diettype',
            name='Name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredienttype',
            name='Name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='mealtype',
            name='Name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='Name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
