# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-02 08:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fpraktikum', '0004_auto_20170730_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='FpCourseFirstHalf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='course name')),
                ('places', models.IntegerField(blank=True, null=True, verbose_name='places')),
                ('graduation', models.CharField(blank=True, choices=[('BA', 'Bachelor'), ('MA', 'Master'), ('L', 'Lehramt')], max_length=2)),
                ('registration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses_first', to='fpraktikum.FpRegistration', verbose_name='semester half')),
            ],
            options={
                'verbose_name': 'course for first semesterhalf',
                'verbose_name_plural': 'courses for first semesterhalf',
            },
        ),
        migrations.CreateModel(
            name='FpCourseSecondHalf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='course name')),
                ('places', models.IntegerField(blank=True, null=True, verbose_name='places')),
                ('graduation', models.CharField(blank=True, choices=[('BA', 'Bachelor'), ('MA', 'Master'), ('L', 'Lehramt')], max_length=2)),
                ('registration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses_second', to='fpraktikum.FpRegistration', verbose_name='semester half')),
            ],
            options={
                'verbose_name': 'course for first semesterhalf',
                'verbose_name_plural': 'courses for first semesterhalf',
            },
        ),
        migrations.CreateModel(
            name='FpUserRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, null=True, verbose_name='user_name')),
                ('user_email', models.EmailField(max_length=254, null=True, verbose_name='user email')),
                ('course_first_half', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fpraktikum.FpCourseFirstHalf', verbose_name='course first semesterhalf')),
                ('course_second_half', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fpraktikum.FpCourseSecondHalf', verbose_name='course second semesterhalf')),
            ],
        ),
        migrations.CreateModel(
            name='FpWaitlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, null=True, verbose_name='user_name')),
                ('user_email', models.EmailField(max_length=254, null=True, verbose_name='user email')),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='registration',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
