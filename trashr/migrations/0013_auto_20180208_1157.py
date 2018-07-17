# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-08 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trashr', '0012_auto_20180204_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('receives_alerts', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='organization',
            name='head_profile',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email_alerts',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trashr.Email'),
        ),
        migrations.AddField(
            model_name='email',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trashr.Organization'),
        ),
    ]