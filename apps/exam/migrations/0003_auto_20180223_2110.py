# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-23 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_auto_20180223_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.TimeField(),
        ),
    ]
