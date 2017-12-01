from rest_framework import serializers

from fpraktikum.models import FpInstitute, FpUserRegistrant, FpUserPartner, FpWaitlist, FpRegistration

from fpraktikum.db_utils import il_db_retrieve, is_user_valid


class FpInstituteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FpInstitute
        fields = ('id', 'name', 'places', 'graduation', 'semesterhalf')

        extra_kwargs = {'id': {'read_only': False}}

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
                  "institutes", "notes")


class FpFullUserRegistrantSerializer(serializers.ModelSerializer):
    """
    This Serializer contains Full information of Registratn + Partner (if set).
    """
    partner = FpLessUserPartnerSerializer(required=False, allow_null=True)
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserRegistrant
        fields = (
            "user_firstname", "user_lastname", "user_matrikel", "partner_has_accepted", "user_mail", "user_login",
            "institutes", "partner", "notes")

    def create(self, validated_data):
        places = 2 if validated_data["partner"] else 1

        institutes = validated_data.pop('institutes')
        partner_data = validated_data.pop('partner')
        partner = None

        user = FpUserRegistrant.objects.create(**validated_data)

        if partner_data:
            del partner_data["institutes"]

            partner = FpUserPartner.objects.create(**partner_data, registrant=user)

        for i in institutes:
            inst = FpInstitute.objects.get(id=i['id'])
            inst.places -= places
            inst.save()
            user.institutes.add(inst)

            if partner:
                partner.institutes.add(inst)

        return user

    def validate(self, data):

        errors = []

        places_needed = 2 if data["partner"] else 1

        #TODO: we encounter a cyclic import here wilth il_db_retrieve and check_user
        if not il_db_retrieve(user_lastname=data['user_lastname'],
                              user_login=data['user_login'],):

            errors.append("Dieser User existiert nicht im Elearning System")

        # Check if User is already Registered

        if not is_user_valid(data["user_login"]):
            errors.append("Der User ist bereits für das Fortgeschrittenen Praktikum eingetragen.")

        if data["partner"]:
            if not il_db_retrieve(user_lastname=data["partner"]['user_lastname'],
                                  user_login=data["partner"]['user_login']):
                errors.append("Dieser User existiert nicht im Elearning System")

            # Check if User is already Registered in any kind

            if not is_user_valid(data["partner"]["user_login"]):
                errors.append("Der User ist bereits für das Fortgeschrittenen Praktikum eingetragen.")

        for institute in data["institutes"]:
            inst = FpInstitute.objects.get(pk=institute["id"])
            if inst.places < places_needed:
                errors.append(u"Im Institut {} stehen nicht mehr genügend Plätze zur Verfügung".format(inst.name))

        if errors:
            raise serializers.ValidationError(errors)
        else:
            return data

    def validate_institutes(self, institutes):
        """
        We Only allow 2 Institutes.
        :param institutes:
        :return:
        """
        errors = []
        if not len(institutes) == 2:
            errors.append(u"Es wurden mehr als 2 oder keine Institute angegeben {}.".format(institutes))
            raise serializers.ValidationError(errors)# if we do not raise it here the next statements will fail. e.g. only 1 institute
        if institutes[0]["semesterhalf"] == 3 or institutes[1]["semesterhalf"]==3:
            errors.append(u"Eines der Institute wird für beide Semesterhälften belegt, bitte wähle nur dieses aus.")
        if institutes[0]["name"] == institutes[1]["name"]:
            errors.append(u"Es müssen 2 unterschiedliche Institute ausgewählt werden.")
        if not institutes[0]["graduation"] == institutes[1]["graduation"]:
            errors.append(u"Es müssen Institute mit dem gleichen Abschluss gewählt werden.")

        for inst in institutes:
            try:
                FpInstitute.objects.get(pk=inst["id"])
            except FpInstitute.DoesNoExist:
                errors.append(u"Das Institut {}, existiert nicht.".format(inst["name"]))

        if errors:
            raise serializers.ValidationError(errors)
        else:
            return institutes


class FpLessUserRegistrantSerializer(serializers.ModelSerializer):
    """
        This Serializer contains Full information of User without partner Field.
    """
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserRegistrant
        fields = (
            "user_firstname", "user_lastname", "user_matrikel", "partner_has_accepted", "user_mail", "user_login",
            "institutes", "notes")


class FpFullUserPartnerSerializer(serializers.ModelSerializer):
    registrant = FpLessUserRegistrantSerializer()
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserPartner
        fields = ("user_firstname", "user_lastname", "user_matrikel", "has_accepted", "user_mail", "user_login",
                  "institutes", "registrant", "notes")


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
