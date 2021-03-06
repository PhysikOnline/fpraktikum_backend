# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-10 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('fpraktikum', '0009_auto_20170817_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fpuserpartner',
            name='user_name',
        ),
        migrations.RemoveField(
            model_name='fpuserregistrant',
            name='user_name',
        ),
        migrations.AddField(
            model_name='fpuserpartner',
            name='has_accepted',
            field=models.BooleanField(default=False, verbose_name='Partner has accepted'),
        ),
        migrations.AddField(
            model_name='fpuserpartner',
            name='user_firstname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='user firstname'),
        ),
        migrations.AddField(
            model_name='fpuserpartner',
            name='user_lastname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='user lastname'),
        ),
        migrations.AddField(
            model_name='fpuserregistrant',
            name='partner_has_accepted',
            field=models.BooleanField(default=False, verbose_name='Partner has accepted'),
        ),
        migrations.AddField(
            model_name='fpuserregistrant',
            name='user_firstname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='user firstname'),
        ),
        migrations.AddField(
            model_name='fpuserregistrant',
            name='user_lastname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='user lastname'),
        ),
    ]
