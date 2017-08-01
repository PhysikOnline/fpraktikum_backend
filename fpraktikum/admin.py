# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import FpRegistration, Course


class CourseAdmin(admin.ModelAdmin):

    list_display = [f.name for f in Course._meta.get_fields()]

admin.site.register(Course, CourseAdmin)


class CourseInline(admin.TabularInline):
    model = Course


class FpRegistrationAdmin(admin.ModelAdmin):

    list_display = [f.name for f in FpRegistration._meta.get_fields()]
    inlines = [
                CourseInline
    ]
admin.site.register(FpRegistration, FpRegistrationAdmin)



