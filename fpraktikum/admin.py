# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import FpRegistration, FpCourseFirstHalf, FpCourseSecondHalf, FpUserRegistration, FpWaitlist


class CourseFirstHalfAdmin(admin.ModelAdmin):

    list_display = [f.name for f in FpCourseFirstHalf._meta.get_fields()]

admin.site.register(FpCourseFirstHalf, CourseFirstHalfAdmin)


class CourseSecondHalfAdmin(admin.ModelAdmin):

    list_display = [f.name for f in FpCourseSecondHalf._meta.get_fields()]

admin.site.register(FpCourseSecondHalf, CourseSecondHalfAdmin)


class FpCourseFirstHalfInline(admin.TabularInline):
    model = FpCourseFirstHalf


class FpCourseSecondHalfInline(admin.TabularInline):
    model = FpCourseSecondHalf


class FpRegistrationAdmin(admin.ModelAdmin):

    list_display = [f.name for f in FpRegistration._meta.get_fields()]
    inlines = [
        FpCourseFirstHalfInline,
        FpCourseSecondHalfInline
    ]
admin.site.register(FpRegistration, FpRegistrationAdmin)


class FpUserRegistrationAdmin(admin.ModelAdmin):

    list_display = [f.name for f in FpUserRegistration._meta.get_fields()]

admin.site.register(FpUserRegistration,FpUserRegistrationAdmin)


class FpWaitlistAdmin(admin.ModelAdmin):
    list_display = [f.name for f in FpWaitlist._meta.get_fields()]

admin.site.register(FpWaitlist,FpWaitlistAdmin)
