# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('fpraktikum', '0002_auto_20170730_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fpregistration',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='enddate of registration'),
        ),
        migrations.AlterField(
            model_name='fpregistration',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='startdate of registration'),
        ),
    ]
