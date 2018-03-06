from rest_framework import serializers

from fpraktikum.models import FpInstitute, FpUserRegistrant, FpUserPartner, FpWaitlist, FpRegistration

from fpraktikum.db_utils import il_db_retrieve, is_user_valid

from fpraktikum.utils import send_email


class FpInstituteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FpInstitute
        fields = ('id', 'name', 'places', 'graduation', 'semesterhalf', 'notes')

        extra_kwargs = {'id': {'read_only': False,
                               'required': False
                               }
                        }


class FpRegistrationSerializer(serializers.ModelSerializer):
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpRegistration
        fields = ('id', 'semester', 'start_date', 'end_date', 'institutes')

    def create(self, validated_data):
        institutes = validated_data.pop('institutes')

        registration = FpRegistration.objects.create(**validated_data)

        for inst in institutes:
            FpInstitute.objects.create(registration=registration, **inst)

        return registration

    def update(self, instance, validated_data):

        # update institutes

        instututes = {}

        if "institutes" in validated_data:

            institutes = validated_data.pop("institutes")

            for institute in institutes:
                inst = instance.institutes.get(pk=institute['id'])
                seri = FpInstituteSerializer(data=institute)
                seri.is_valid(raise_exception=True)
                seri.update(inst, seri.validated_data)

        return super(FpRegistrationSerializer, self).update(instance, validated_data)


class FpLessUserPartnerSerializer(serializers.ModelSerializer):
    """
    This Serializer contains Full information of Partner without registrant Field.
    """
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserPartner
        fields = ('id', "user_firstname", "user_lastname", "user_matrikel", "has_accepted", "user_mail", "user_login",
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
            "id", "user_firstname", "user_lastname", "user_matrikel", "partner_has_accepted", "user_mail", "user_login",
            "institutes", "partner", "notes")

    def create(self, validated_data):
        places = 2 if validated_data["partner"] else 1

        institutes = validated_data.pop('institutes')
        partner_data = validated_data.pop('partner')
        partner = None

        user = FpUserRegistrant.objects.create(**validated_data)

        if partner_data:
            del partner_data["institutes"]

            partner = FpUserPartner.objects.create(registrant=user, **partner_data)

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
        But there is one, and only one, case where 1 Institute is allowed.
        This case is, if a student has graduation "L" (Lehramt)
        :param institutes:
        :return:
        """

        errors = []

        if len(institutes) == 1 and institutes[0]["graduation"] == "L":
            # if the student is a "Lehramt" candidate
            # no checks needed
            pass
        else:

            if not (len(institutes) == 2):
                errors.append(u"Es wurden mehr als 2 oder keine Institute angegeben {}.".format(institutes))
                raise serializers.ValidationError(errors) # if we do not raise it here the next statements will fail. e.g. only 1 institute
            if institutes[0]["semesterhalf"] == 3 or institutes[1]["semesterhalf"]==3:
                errors.append(u"Eines der Institute wird für beide Semesterhälften belegt, bitte wähle nur dieses aus.")
            if institutes[0]["name"] == institutes[1]["name"]:
                errors.append(u"Es müssen 2 unterschiedliche Institute ausgewählt werden.")
            if not institutes[0]["graduation"] == institutes[1]["graduation"]:
                errors.append(u"Es müssen Institute mit dem gleichen Abschluss gewählt werden.")

        for inst in institutes:
            try:
                FpInstitute.objects.get(pk=inst["id"])
            except FpInstitute.DoesNotExist:
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
            'id', "user_firstname", "user_lastname", "user_matrikel", "partner_has_accepted", "user_mail", "user_login",
            "institutes", "notes")


class FpFullUserPartnerSerializer(serializers.ModelSerializer):
    registrant = FpLessUserRegistrantSerializer()
    institutes = FpInstituteSerializer(many=True)

    class Meta:
        model = FpUserPartner
        fields = ('id', "user_firstname", "user_lastname", "user_matrikel", "has_accepted", "user_mail", "user_login",
                  "institutes", "registrant", "notes")


class FpWaitlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = FpWaitlist
        fields = "__all__"


class DummySerializer(serializers.Serializer):
    pass
