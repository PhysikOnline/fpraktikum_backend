# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-02 11:21
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('fpraktikum', '0007_fpuserregistration_partner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fpuserregistration',
            options={'verbose_name': 'registration', 'verbose_name_plural': 'registrations'},
        ),
        migrations.AlterField(
            model_name='fpuserregistration',
            name='course_first_half',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='fpraktikum.FpCourseFirstHalf', verbose_name='course first semesterhalf'),
        ),
        migrations.AlterField(
            model_name='fpuserregistration',
            name='course_second_half',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='fpraktikum.FpCourseSecondHalf', verbose_name='course second semesterhalf'),
        ),
        migrations.AlterField(
            model_name='fpuserregistration',
            name='partner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='registrant_user', to='fpraktikum.FpUserRegistration'),
        ),
        migrations.AlterField(
            model_name='fpuserregistration',
            name='user_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='user email'),
        ),
        migrations.AlterField(
            model_name='fpuserregistration',
            name='user_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='user name'),
        ),
    ]
