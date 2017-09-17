# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-13 01:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20170831_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='dumpster',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='dumpster',
            name='capacity_units',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='dumpster',
            name='container_type',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='dumpster',
            name='location',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='dumpster',
            name='rfid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dumpster',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
    ]