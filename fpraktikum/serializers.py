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


