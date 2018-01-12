# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


from django.db import models


class UsrData(models.Model):
    usr_id = models.IntegerField(primary_key=True)
    login = models.CharField(unique=True, max_length=80, blank=True, null=True)
    passwd = models.CharField(max_length=80, blank=True, null=True)
    firstname = models.CharField(max_length=32, blank=True, null=True)
    lastname = models.CharField(max_length=32, blank=True, null=True)
    title = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    institution = models.CharField(max_length=80, blank=True, null=True)
    street = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=40, blank=True, null=True)
    phone_office = models.CharField(max_length=40, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    hobby = models.CharField(max_length=4000, blank=True, null=True)
    department = models.CharField(max_length=80, blank=True, null=True)
    phone_home = models.CharField(max_length=40, blank=True, null=True)
    phone_mobile = models.CharField(max_length=40, blank=True, null=True)
    fax = models.CharField(max_length=40, blank=True, null=True)
    time_limit_owner = models.IntegerField(blank=True, null=True)
    time_limit_unlimited = models.IntegerField(blank=True, null=True)
    time_limit_from = models.IntegerField(blank=True, null=True)
    time_limit_until = models.IntegerField(blank=True, null=True)
    time_limit_message = models.IntegerField(blank=True, null=True)
    referral_comment = models.CharField(max_length=250, blank=True, null=True)
    matriculation = models.CharField(max_length=40, blank=True, null=True)
    active = models.IntegerField()
    approve_date = models.DateTimeField(blank=True, null=True)
    agree_date = models.DateTimeField(blank=True, null=True)
    client_ip = models.CharField(max_length=255, blank=True, null=True)
    auth_mode = models.CharField(max_length=10, blank=True, null=True)
    profile_incomplete = models.IntegerField(blank=True, null=True)
    ext_account = models.CharField(max_length=250, blank=True, null=True)
    im_icq = models.CharField(max_length=40, blank=True, null=True)
    im_yahoo = models.CharField(max_length=40, blank=True, null=True)
    im_msn = models.CharField(max_length=40, blank=True, null=True)
    im_aim = models.CharField(max_length=40, blank=True, null=True)
    im_skype = models.CharField(max_length=40, blank=True, null=True)
    feed_hash = models.CharField(max_length=32, blank=True, null=True)
    delicious = models.CharField(max_length=40, blank=True, null=True)
    latitude = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)
    loc_zoom = models.IntegerField()
    login_attempts = models.IntegerField()
    last_password_change = models.IntegerField()
    im_jabber = models.CharField(max_length=40, blank=True, null=True)
    im_voip = models.CharField(max_length=40, blank=True, null=True)
    reg_hash = models.CharField(max_length=32, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    sel_country = models.CharField(max_length=2, blank=True, null=True)
    last_visited = models.TextField(blank=True, null=True)
    inactivation_date = models.DateTimeField(blank=True, null=True)
    is_self_registered = models.IntegerField()
    passwd_enc_type = models.CharField(max_length=10, blank=True, null=True)
    passwd_salt = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usr_data'
