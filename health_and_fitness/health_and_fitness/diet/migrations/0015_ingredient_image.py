# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-14 00:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0014_auto_20170214_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='Image',
            field=models.ImageField(default=b'ingre_image/default.jpg', upload_to=b'ingre_image/'),
        ),
    ]
