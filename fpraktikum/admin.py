# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

from .models import FpRegistration, FpUserRegistrant, FpUserPartner, FpWaitlist, FpInstitute


class FpInstituteAdmin(admin.ModelAdmin):

    list_display = ['name', 'places', 'graduation', 'get_registration', 'semesterhalf']

    def get_registration(self, obj):
        return obj.registration.semester

admin.site.register(FpInstitute, FpInstituteAdmin)


class FpInstituteInline(admin.TabularInline):
    model = FpInstitute


class FpUserPartnerAdmin(admin.ModelAdmin):
    list_display = ("user_firstname", "user_lastname", "user_matrikel", "has_accepted", "user_mail", "user_login",
                    "get_institutes", "registrant")

    def get_institutes(self, obj):
        return "\n".join([p.name for p in obj.institutes.all()])

admin.site.register(FpUserPartner, FpUserPartnerAdmin)


class FpRegistrationAdmin(admin.ModelAdmin):

    list_display = ['semester', 'start_date', 'end_date']
    inlines = [
        FpInstituteInline,
    ]

admin.site.register(FpRegistration, FpRegistrationAdmin)


class RegistrantResource(resources.ModelResource):
    # partner__user_firstname = fields.Field(column_name="partner firstname")
    # partner__user_lastname = fields.Field(column_name="partner lastname")
    # partner__user_matrikel = fields.Field(column_name="partner matrikel")
    institute_semesterhalf = fields.Field()
    institute_graduation = fields.Field()

    class Meta:
        model = FpUserRegistrant
        fields = ("user_firstname", "user_lastname", "user_matrikel", "partner_has_accepted",
                  "partner__user_firstname", "partner__user_lastname", "partner__user_matrikel",
                  )
        export_order = ("user_firstname", "user_lastname", "user_matrikel", "partner_has_accepted",
                        "institute_semesterhalf", "institute_graduation", "partner__user_firstname",
                        "partner__user_lastname", "partner__user_matrikel", )

    def dehydrate_institute_semesterhalf(self, registrant):
        institutes = registrant.institutes.all()
        string = ""
        for inst in institutes:
            string += "name: {} semesterhalf: {},".format(inst.name, inst.semesterhalf)
        return string

    def dehydrate_institute_graduation(self, registrant):
        institutes = registrant.institutes.all()
        return " {}".format(institutes[0].graduation)

    def dehydrate_partner_has_accepted(self, registrant):
        return "Yes" if registrant.partner_has_accepted else "No"

class FpUserRegistrantAdmin(ImportExportModelAdmin):
    list_display = (
    "user_firstname", "user_lastname", "user_matrikel", "partner_has_accepted", "user_mail", "user_login",
    "get_institutes", "partner")

    resource_class = RegistrantResource

    def get_institutes(self, obj):
        return "\n".join([p.name for p in obj.institutes.all()])

admin.site.register(FpUserRegistrant, FpUserRegistrantAdmin)


class FpWaitlistAdmin(admin.ModelAdmin):

    list_display = [f.name for f in FpWaitlist._meta.get_fields()]

admin.site.register(FpWaitlist, FpWaitlistAdmin)


