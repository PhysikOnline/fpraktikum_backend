from rest_framework import serializers

from fpraktikum.models import *


class FpInstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FpInstitute
        fields = ('name', 'places', 'graduation', 'semester_half')


class FpRegistrationSerializer(serializers.ModelSerializer):

    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpRegistration
        fields = ('semester', 'start_date', 'end_date', 'institutes')


class FpLessUserPartnerSerializer(serializers.ModelSerializer):
    """
    This Serializer contains Full information of Partner without registrant Field.
    """
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserPartner
        fields = ("user_firstname", "user_lastname", "has_accepted", "user_email", "user_login", "institutes")


class FpFullUserRegistrantSerializer(serializers.ModelSerializer):
    """
    This Serializer contains Full information of Registratn + Partner (if set).
    """
    partner = FpLessUserPartnerSerializer()
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserRegistrant
        fields = ("user_firstname", "user_lastname", "partner_has_accepted", "user_email", "user_login", "institutes",
                  "partner")


class FpLessUserRegistrantSerializer(serializers.ModelSerializer):
    """
        This Serializer contains Full information of User without partner Field.
    """
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserRegistrant
        fields = ("user_firstname", "user_lastname", "partner_has_accepted", "user_email", "user_login", "institutes")


class FpFullUserPartnerSerializer(serializers.ModelSerializer):
    registrant = FpLessUserRegistrantSerializer()
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserPartner
        fields = ("user_firstname", "user_lastname", "has_accepted", "user_email", "user_login", "institutes",
                  "registrant")

class InstituteSerializer(serializers.Serializer):
    name= serializers.CharField()
    gradiuation= serializers.CharField()
    semesterhalf= serializers.IntegerField()
class PartnerSerializer(serializers.Serializer):
    user_firstname = serializers.CharField()
    user_lastname = serializers.CharField()
    user_login = serializers.CharField()
    user_mail = serializers.CharField()


class DemoSerializer(serializers.Serializer):
    user_firstname= serializers.CharField()
    user_lastname= serializers.CharField()
    user_login= serializers.CharField()
    user_mail= serializers.CharField()
    institutes = InstituteSerializer(many=True)
    partner = PartnerSerializer()

class AcceptDeclineSerializer(serializers.Serializer):
    user_firstname = serializers.CharField()
    user_lastname = serializers.CharField()
    user_login = serializers.CharField()
    user_mail = serializers.CharField()
    accept_decline = serializers.BooleanField()

