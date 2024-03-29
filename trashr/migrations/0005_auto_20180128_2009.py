# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-29 01:09
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trashr', '0004_remove_organization_activated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervalreading',
            name='raw_reading',
        ),
        migrations.AddField(
            model_name='dumpster',
            name='coreid',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AddField(
            model_name='intervalreading',
            name='raw_readings',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.SmallIntegerField(default=0), default=[], size=None),
            preserve_default=False,
        ),
    ]
