# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-05 04:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trashr', '0009_auto_20180204_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='Dumpster',
        ),
        migrations.DeleteModel(
            name='Alert',
        ),
    ]
