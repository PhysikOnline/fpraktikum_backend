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


class FpCourseFirstHalf(models.Model):
    GRADUATION_CHOICES = (("BA", "Bachelor"), ("MA", "Master"), ("L", "Lehramt"))

    name = models.CharField(verbose_name=_("course name"),
                            max_length=100)

    places = models.IntegerField(verbose_name=_("places"),
                                 blank=True,
                                 null=True)
    graduation = models.CharField(max_length=2,
                                  choices=GRADUATION_CHOICES,
                                  blank=True)
    registration = models.ForeignKey(FpRegistration,
                                     verbose_name=_("semester half"),
                                     related_name="courses_first",
                                     null=True)

    class Meta:
        verbose_name = _("course for first semesterhalf")
        verbose_name_plural = _("courses for first semesterhalf")

    def __unicode__(self):
        return self.name


class FpCourseSecondHalf(models.Model):
    GRADUATION_CHOICES = (("BA", "Bachelor"), ("MA", "Master"), ("L", "Lehramt"))

    name = models.CharField(verbose_name=_("course name"),
                            max_length=100)

    places = models.IntegerField(verbose_name=_("places"),
                                 blank=True,
                                 null=True)
    graduation = models.CharField(max_length=2,
                                  choices=GRADUATION_CHOICES,
                                  blank=True)
    registration = models.ForeignKey(FpRegistration,
                                     verbose_name=_("semester half"),
                                     related_name="courses_second",
                                     null=True)

    class Meta:
        verbose_name = _("course for second semesterhalf")
        verbose_name_plural = _("courses for second semesterhalf")

    def __unicode__(self):
        return self.name


class FpUserRegistration(models.Model):

    user_name = models.CharField(max_length=100,
                                 verbose_name=_("user name"),
                                 null=True,
                                 blank=True)
    user_email = models.EmailField(verbose_name=_("user email"),
                                   null=True, blank=True)
    course_first_half = models.ForeignKey(FpCourseFirstHalf,
                                          verbose_name=_("course first semesterhalf"),
                                          null=True,
                                          blank=True)
    course_second_half = models.ForeignKey(FpCourseSecondHalf,
                                           verbose_name=_("course second semesterhalf"),
                                           null=True,
                                           blank=True)
    partner = models.OneToOneField('self', unique=True, related_name="registrant_user", null=True, blank=True)

    class Meta:
        verbose_name = _("registration")
        verbose_name_plural = _("registrations")

    def __unicode__(self):
        return self.user_name


class FpWaitlist(models.Model):

    user_name = models.CharField(max_length=100,
                                 verbose_name=_("user name"),
                                 null=True)
    user_email = models.EmailField(verbose_name=_("user email"),
                                   null=True)
    # wish_course_1 = ''
    #
    # wish_course_2 = ''














