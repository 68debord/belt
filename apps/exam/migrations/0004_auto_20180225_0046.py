# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-25 00:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_auto_20180223_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.CharField(max_length=255)),
                ('quoted_by', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='creator',
        ),
        migrations.AddField(
            model_name='user',
            name='alias',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.AddField(
            model_name='quote',
            name='fav_users',
            field=models.ManyToManyField(related_name='fave_quotes', to='exam.User'),
        ),
        migrations.AddField(
            model_name='quote',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_quotes', to='exam.User'),
        ),
    ]