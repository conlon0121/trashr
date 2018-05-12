# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-10 21:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trashr', '0019_auto_20180509_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmethod',
            name='default',
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='customer_id',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trashr.UserProfile'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trashr.PaymentMethod'),
        ),
    ]
