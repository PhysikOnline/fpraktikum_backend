# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-12 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fpraktikum', '0010_auto_20170910_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsrData',
            fields=[
                ('usr_id', models.IntegerField(primary_key=True, serialize=False)),
                ('login', models.CharField(blank=True, max_length=80, null=True, unique=True)),
                ('passwd', models.CharField(blank=True, max_length=80, null=True)),
                ('firstname', models.CharField(blank=True, max_length=32, null=True)),
                ('lastname', models.CharField(blank=True, max_length=32, null=True)),
                ('title', models.CharField(blank=True, max_length=32, null=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('email', models.CharField(blank=True, max_length=80, null=True)),
                ('institution', models.CharField(blank=True, max_length=80, null=True)),
                ('street', models.CharField(blank=True, max_length=40, null=True)),
                ('city', models.CharField(blank=True, max_length=40, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=10, null=True)),
                ('country', models.CharField(blank=True, max_length=40, null=True)),
                ('phone_office', models.CharField(blank=True, max_length=40, null=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('last_update', models.DateTimeField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('hobby', models.CharField(blank=True, max_length=4000, null=True)),
                ('department', models.CharField(blank=True, max_length=80, null=True)),
                ('phone_home', models.CharField(blank=True, max_length=40, null=True)),
                ('phone_mobile', models.CharField(blank=True, max_length=40, null=True)),
                ('fax', models.CharField(blank=True, max_length=40, null=True)),
                ('time_limit_owner', models.IntegerField(blank=True, null=True)),
                ('time_limit_unlimited', models.IntegerField(blank=True, null=True)),
                ('time_limit_from', models.IntegerField(blank=True, null=True)),
                ('time_limit_until', models.IntegerField(blank=True, null=True)),
                ('time_limit_message', models.IntegerField(blank=True, null=True)),
                ('referral_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('matriculation', models.CharField(blank=True, max_length=40, null=True)),
                ('active', models.IntegerField()),
                ('approve_date', models.DateTimeField(blank=True, null=True)),
                ('agree_date', models.DateTimeField(blank=True, null=True)),
                ('client_ip', models.CharField(blank=True, max_length=255, null=True)),
                ('auth_mode', models.CharField(blank=True, max_length=10, null=True)),
                ('profile_incomplete', models.IntegerField(blank=True, null=True)),
                ('ext_account', models.CharField(blank=True, max_length=250, null=True)),
                ('im_icq', models.CharField(blank=True, max_length=40, null=True)),
                ('im_yahoo', models.CharField(blank=True, max_length=40, null=True)),
                ('im_msn', models.CharField(blank=True, max_length=40, null=True)),
                ('im_aim', models.CharField(blank=True, max_length=40, null=True)),
                ('im_skype', models.CharField(blank=True, max_length=40, null=True)),
                ('feed_hash', models.CharField(blank=True, max_length=32, null=True)),
                ('delicious', models.CharField(blank=True, max_length=40, null=True)),
                ('latitude', models.CharField(blank=True, max_length=30, null=True)),
                ('longitude', models.CharField(blank=True, max_length=30, null=True)),
                ('loc_zoom', models.IntegerField()),
                ('login_attempts', models.IntegerField()),
                ('last_password_change', models.IntegerField()),
                ('im_jabber', models.CharField(blank=True, max_length=40, null=True)),
                ('im_voip', models.CharField(blank=True, max_length=40, null=True)),
                ('reg_hash', models.CharField(blank=True, max_length=32, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('sel_country', models.CharField(blank=True, max_length=2, null=True)),
                ('last_visited', models.TextField(blank=True, null=True)),
                ('inactivation_date', models.DateTimeField(blank=True, null=True)),
                ('is_self_registered', models.IntegerField()),
                ('passwd_enc_type', models.CharField(blank=True, max_length=10, null=True)),
                ('passwd_salt', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'db_table': 'usr_data',
                'managed': False,
            },
        ),
        migrations.RenameField(
            model_name='fpuserpartner',
            old_name='user_snumber',
            new_name='user_login',
        ),
        migrations.RenameField(
            model_name='fpuserregistrant',
            old_name='user_snumber',
            new_name='user_login',
        ),
        migrations.AlterField(
            model_name='fpinstitute',
            name='places',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='places'),
        ),
    ]
