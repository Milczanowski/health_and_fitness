# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-13 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0012_meal_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='Image',
            field=models.ImageField(default=b'meals_image/default.jpg', upload_to=b'meals_image/'),
        ),
    ]