# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _


class FpRegistration(models.Model):

    semester = models.CharField(default='WS17',
                                max_length=4,
                                verbose_name=_("semester"),
                                blank=True)
    start_date = models.DateTimeField(verbose_name=_("startdate of registration"),
                                      null=True)
    end_date = models.DateTimeField(verbose_name=_("enddate of registration"),
                                    null=True)

    class Meta:
        verbose_name = _("FP registration")
        verbose_name_plural = _("Fp registrations")

    def __unicode__(self):
        return _("fp registration")


class Course(models.Model):
    GRADUATION_CHOICES = (("BA", "Bachelor"), ("MA", "Master"), ("L", "Lehramt"))

    registration = models.ForeignKey(FpRegistration,
                                      verbose_name=_("semester half"),
                                      related_name="courses",
                                      null=True)

    name = models.CharField(verbose_name=_("course name"),
                            max_length=100)

    places = models.IntegerField(verbose_name=_("places"),
                                 blank=True,
                                 null=True)
    graduation = models.CharField(max_length=2,
                                  choices=GRADUATION_CHOICES,
                                  blank=True)
    semester_half= models.IntegerField(verbose_name=_("semester half"),
                                       choices=((1, 1), (2, 2)),
                                       null=True)
    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __unicode__(self):
        return self.name














