# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-21 03:25
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_route'),
    ]

    operations = [
        CreateExtension('postgis'),
        migrations.RemoveField(
            model_name='dumpster',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='dumpster',
            name='longitude',
        ),
        migrations.AddField(
            model_name='dumpster',
            name='lat_long',
            field=django.contrib.gis.db.models.fields.PointField(default=0, srid=4326),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.MultiPointField(default=0, srid=4326),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='route',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
