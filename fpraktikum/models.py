# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fpraktikum.utils import get_semester


class FpRegistration(models.Model):

    semester = models.CharField(default=get_semester(),
                                max_length=4,
                                verbose_name=_("semester"),
                                blank=True)
    start_date = models.DateTimeField(verbose_name=_("startdate of registration"),
                                      )
    end_date = models.DateTimeField(verbose_name=_("enddate of registration"),
                                    )

    class Meta:
        verbose_name = _("FP registration")
        verbose_name_plural = _("Fp registrations")

    def __unicode__(self):
        return self.semester


class FpInstitute(models.Model):
    GRADUATION_CHOICES = (("BA", "Bachelor"), ("MA", "Master"), ("L", "Lehramt"))

    SEMESTER_HALF = ((1, "1."), (2, "2."), (3, _("both")))

    name = models.CharField(verbose_name=_("course name"),
                            max_length=100
                            )

    places = models.IntegerField(default=0,
                                 verbose_name=_("places"),
                                 blank=True,

                                 )

    graduation = models.CharField(max_length=2,
                                  choices=GRADUATION_CHOICES,
                                  blank=True
                                  )

    registration = models.ForeignKey(FpRegistration,
                                     verbose_name=_("registration"),
                                     related_name="institutes",
                                     blank=True
                                     )

    semesterhalf = models.IntegerField(verbose_name=_("semester half"),
                                        blank=True,
                                        choices=SEMESTER_HALF
                                        )

    class Meta:
        verbose_name = _("institute")
        verbose_name_plural = _("institutes")

    def __unicode__(self):
        return self.name


class FpUserRegistrant(models.Model):
    user_firstname = models.CharField(max_length=100,
                                      verbose_name=_("user firstname"),
                                      blank=True
                                      )
    user_lastname = models.CharField(max_length=100,
                                     verbose_name=_("user lastname"),
                                     blank=True
                                     )
    partner_has_accepted = models.BooleanField(default=False,
                                               verbose_name=_("Partner has accepted"))
    user_mail = models.EmailField(verbose_name=_("user email"),
                                   blank=True
                                   )
    user_login = models.CharField(max_length=100,
                                  verbose_name=_("s number / login"),
                                  blank=True
                                  )
    user_matrikel = models.CharField(max_length=100,
                                     verbose_name=_("Matrikelnumber"),
                                     blank=True
                                     )
    institutes = models.ManyToManyField(FpInstitute,
                                        verbose_name=_("institutes"),
                                        blank=True
                                        )
    @classmethod
    def create_from_partner(cls, partner):
        user = cls(user_firstname=partner.user_firstname,
                   user_lastname=partner.user_lastname,
                   user_login=partner.user_login,
                   user_email=partner.user_email,
                   user_matrikel=partner.user_matrikel,
                   )
        user.save()
        user.institutes.set(partner.institutes.all())
        return user

    class Meta:
        verbose_name = _("User/Registrant")
        verbose_name_plural = _("Users/Registrants")
        unique_together = (('user_firstname', 'user_lastname', 'user_mail', 'user_login', 'user_matrikel'),)

    def __unicode__(self):
        return self.user_lastname


class FpUserPartner(models.Model):
    user_firstname = models.CharField(max_length=100,
                                      verbose_name=_("user firstname"),
                                      blank=True
                                      )
    user_lastname = models.CharField(max_length=100,
                                     verbose_name=_("user lastname"),
                                     blank=True
                                     )
    has_accepted = models.BooleanField(default=False,
                                       verbose_name=_("Has accepted"))
    user_mail = models.EmailField(verbose_name=_("user email"),
                                   blank=True
                                   )
    user_login = models.CharField(max_length=100,
                                  verbose_name=_("s number / login"),
                                  blank=True
                                  )
    user_matrikel = models.CharField(max_length=100,
                                     verbose_name=_("Matrikelnumber"),
                                     blank=True
                                     )
    institutes = models.ManyToManyField(FpInstitute,
                                        verbose_name=_("institutes"),
                                        blank=True
                                        )
    registrant = models.OneToOneField(FpUserRegistrant,
                                      verbose_name=_("registrant"),
                                      related_name="partner",
                                      blank=True,
                                      )

    class Meta:
        verbose_name = _("User/Partner")
        verbose_name_plural = _("Users/Partners")
        unique_together = (('user_firstname', 'user_lastname', 'user_mail', 'user_login', 'user_matrikel'),)

    def __unicode__(self):
        return self.user_lastname


class FpWaitlist(models.Model):
    GRADUATION_CHOICES = (("BA", "Bachelor"), ("MA", "Master"), ("L", "Lehramt"))

    user_firstname = models.CharField(max_length=100,
                                      verbose_name=_("user firstname"),
                                      )
    user_lastname = models.CharField(max_length=100,
                                     verbose_name=_("user lastname"),
                                     )
    user_mail = models.EmailField(verbose_name=_("user email"),
                                   )
    user_login = models.CharField(max_length=100,
                                  verbose_name=_("s number / login"),
                                  blank=True)
    user_matrikel = models.CharField(max_length=100,
                                     verbose_name=_("Matrikelnummer"),
                                     blank=True)
    graduation = models.CharField(max_length=2,
                                  choices=GRADUATION_CHOICES,
                                  blank=True
                                  )

    class Meta:
        verbose_name = _("Waitlist")
        verbose_name_plural = _("Waitlists")
        unique_together = (('user_firstname', 'user_lastname', 'user_mail', 'user_login', 'user_matrikel'),)














