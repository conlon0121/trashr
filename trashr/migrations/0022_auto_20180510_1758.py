# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-10 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trashr', '0021_remove_paymentmethod_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='card_id',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
