# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-05 04:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trashr', '0010_auto_20180204_2319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fill_percent', models.PositiveSmallIntegerField(default=70)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('Dumpster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trashr.Dumpster')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trashr.Organization')),
            ],
        ),
    ]
