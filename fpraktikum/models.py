# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _
from .utils import get_semester


class FpRegistration(models.Model):

    semester = models.CharField(default=get_semester(),
                                max_length=4,
                                verbose_name=_("semester"),
                                blank=True)
    start_date = models.DateTimeField(verbose_name=_("startdate of registration"),
                                      null=True)
    end_date = models.DateTimeField(verbose_name=_("enddate of registration"),
                                    null=True)
    notes = models.

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

    places = models.IntegerField(verbose_name=_("places"),
                                 blank=True,
                                 null=True
                                 )

    graduation = models.CharField(max_length=2,
                                  choices=GRADUATION_CHOICES,
                                  blank=True
                                  )

    registration = models.ForeignKey(FpRegistration,
                                     verbose_name=_("registration"),
                                     related_name="institutes",
                                     null=True,
                                     blank=True
                                     )

    semester_half = models.IntegerField(verbose_name=_("semester half"),
                                        blank=True,
                                        null=True,
                                        choices=SEMESTER_HALF
                                        )

    class Meta:
        verbose_name = _("institute")
        verbose_name_plural = _("institutes")

    def __unicode__(self):
        return self.name


class FpUserPartner(models.Model):

    user_name = models.CharField(max_length=100,
                                 verbose_name=_("user name"),
                                 null=True,
                                 blank=True
                                 )
    user_email = models.EmailField(verbose_name=_("user email"),
                                   null=True, blank=True
                                   )
    user_snumber = models.CharField(max_length=100,
                                    verbose_name=_("s number / login"),
                                    null=True,
                                    blank=True
                                    )
    institutes = models.ForeignKey(FpInstitute,
                                   verbose_name=_("institutes"),
                                   null=True,
                                   blank=True
                                   )

    class Meta:
        verbose_name = _("User/Partner")
        verbose_name_plural = _("Users/Partners")

    def __unicode__(self):
        return self.user_name


class FpUserRegistrant(models.Model):

    user_name = models.CharField(max_length=100,
                                 verbose_name=_("user name"),
                                 null=True,
                                 blank=True
                                 )
    user_email = models.EmailField(verbose_name=_("user email"),
                                   null=True, blank=True
                                   )
    user_snumber = models.CharField(max_length=100,
                                    verbose_name=_("s number / login"),
                                    null=True,
                                    blank=True
                                    )
    institutes = models.ForeignKey(FpInstitute,
                                   verbose_name=_("institutes"),
                                   null=True,
                                   blank=True
                                   )
    partner = models.OneToOneField(FpUserPartner,
                                   verbose_name=_("partner"),
                                   related_name="registrant",
                                   null=True,
                                   blank=True
                                   )

    class Meta:
        verbose_name = _("User/Registrant")
        verbose_name_plural = _("Users/Registrants")

    def __unicode__(self):
        return self.user_name


class FpWaitlist(models.Model):

    user_name = models.CharField(max_length=100,
                                 verbose_name=_("user name"),
                                 null=True)
    user_email = models.EmailField(verbose_name=_("user email"),
                                   null=True)
    user_snumber = models.CharField(max_length=100,
                                    verbose_name=_("s number / login"),
                                    null=True,
                                    blank=True)















