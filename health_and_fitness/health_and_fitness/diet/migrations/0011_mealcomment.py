# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-13 23:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diet', '0010_auto_20170213_2358'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Content', models.TextField(default=b'')),
                ('Creation_Data', models.DateTimeField(default=django.utils.timezone.now)),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diet.Meal')),
            ],
        ),
    ]
