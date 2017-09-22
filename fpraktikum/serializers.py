from rest_framework import serializers

from fpraktikum.models import FpInstitute, FpUserRegistrant, FpUserPartner, FpWaitlist, FpRegistration


class FpInstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FpInstitute
        fields = ('name', 'places', 'graduation', 'semesterhalf')


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
        fields = ("user_firstname", "user_lastname", "user_matrikel", "has_accepted", "user_mail", "user_login",
                  "institutes")


class FpFullUserRegistrantSerializer(serializers.ModelSerializer):
    """
    This Serializer contains Full information of Registratn + Partner (if set).
    """
    partner = FpLessUserPartnerSerializer()
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserRegistrant
        fields = (
        "user_firstname", "user_lastname", "user_matrikel", "partner_has_accepted", "user_mail", "user_login",
        "institutes", "partner")


class FpLessUserRegistrantSerializer(serializers.ModelSerializer):
    """
        This Serializer contains Full information of User without partner Field.
    """
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserRegistrant
        fields = (
        "user_firstname", "user_lastname", "user_matrikel", "partner_has_accepted", "user_mail", "user_login",
        "institutes")


class FpFullUserPartnerSerializer(serializers.ModelSerializer):
    registrant = FpLessUserRegistrantSerializer()
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserPartner
        fields = ("user_firstname", "user_lastname", "user_matrikel", "has_accepted", "user_mail", "user_login",
                  "institutes", "registrant")


class FpWaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = FpWaitlist
        fields = '__all__'


class InstituteSerializer(serializers.Serializer):
    name = serializers.CharField()
    graduation = serializers.CharField()
    semesterhalf = serializers.IntegerField()


class PartnerSerializer(serializers.Serializer):
    user_firstname = serializers.CharField()
    user_lastname = serializers.CharField()
    user_login = serializers.CharField()
    user_mail = serializers.EmailField()
    user_matrikel = serializers.CharField()


class RegistrationSerializer(serializers.Serializer):
    user_firstname = serializers.CharField()
    user_lastname = serializers.CharField()
    user_login = serializers.CharField()
    user_mail = serializers.EmailField()
    user_matrikel = serializers.CharField()
    institutes = InstituteSerializer(many=True)
    partner = PartnerSerializer(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=1000)

    def validate_institutes(self, value):
        """
        Check that there are one or two Institutes given
        :param value:
        :return:
        """

        if not 1 <= len(value) <= 2:
            raise serializers.ValidationError("Es wurden mehr als 2 oder keine Institute angegeben.")
        return value


class AcceptDeclineSerializer(serializers.Serializer):
    user_firstname = serializers.CharField()
    user_lastname = serializers.CharField()
    user_login = serializers.CharField()
    user_mail = serializers.EmailField()
    user_matrikel = serializers.CharField()
    accept = serializers.BooleanField()


class CheckPartnerSerializer(serializers.Serializer):
    user_lastname = serializers.CharField()
    user_login = serializers.CharField()

class WaitlistSerializer(serializers.Serializer):
    user_firstname = serializers.CharField()
    user_lastname = serializers.CharField()
    user_login = serializers.CharField()
    user_mail = serializers.EmailField()
    user_matrikel = serializers.CharField()
    graduation = serializers.CharField()
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=1000)