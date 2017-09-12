from rest_framework import generics, status
from .models import *
from .serializers import *
from fpraktikum.utils import get_semester, il_db_retrieve
from django.shortcuts import get_object_or_404

from rest_framework.response import Response


class RegistrationView(generics.RetrieveAPIView):
    queryset = FpRegistration.objects.all()
    serializer_class = FpRegistrationSerializer
    name = 'registration'
    lookup_field = None

    def get_object(self):
        current_semester = get_semester()
        obj = self.get_queryset().filter(semester=current_semester)
        obj = get_object_or_404(obj)
        return obj


class UserCheckView(generics.RetrieveAPIView):
    name = 'user'
    lookup_field = 'user_login'
    queryset = FpUserRegistrant.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        semester = get_semester()
        # Perform the lookup filtering.
        lookup_field = self.lookup_field

        is_registrant = FpUserRegistrant.objects.filter(user_login=self.kwargs[lookup_field],
                                                        institutes__registration__semester=semester)
        is_partner = FpUserPartner.objects.filter(user_login=self.kwargs[lookup_field],
                                                  institutes__registration__semester=semester)
        if is_registrant:
            obj = is_registrant.distinct(lookup_field).get()
            serializer = FpFullUserRegistrantSerializer(obj)
            response = Response(serializer.data)
            response.data["status"] = "registrant"
            return response

        elif is_partner:
            obj = is_partner.distinct(lookup_field).get()
            serializer = FpFullUserPartnerSerializer(obj)
            response = Response(serializer.data)
            response.data["status"] = "partner"
            return response
        else:
            data = {"status": None}
            return Response(data)

        # filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        # obj = get_object_or_404(queryset, **filter_kwargs)


class TestIlDbView(generics.RetrieveAPIView):
    name = 'ilias_db'
    queryset = FpRegistration.objects.all()
    serializer_class = FpRegistrationSerializer

    def get(self, request, *args, **kwargs):

        get_params = request.GET
        result = il_db_retrieve(user_firstname=get_params['user_firstname'], user_lastname=get_params['user_lastname'],
                                user_login=get_params['user_login'], user_mail=get_params['user_mail'])
        if result:
            return Response(data={'data': result}, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetRegistrationView(generics.CreateAPIView):
    name = 'set_registration'
    queryset = FpUserRegistrant.objects.all()
    serializer_class = FpFullUserRegistrantSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        semester = get_semester()
        institute_one = FpInstitute()  # we define an empty class for acces purpose later on
        institute_two = FpInstitute()  # we define an empty class for acces purpose later on
        if data["user_firstname"] and data["user_lastname"] and data["user_login"] and data["user_mail"]:
            # we want to be sure that this data is atleast provided
            if il_db_retrieve(user_firstname=data["user_firstname"], user_lastname=data["user_lastname"],
                              user_login=data["user_login"], user_mail=data["user_mail"]):
                # we want to know if this user actually exists in the elearning system

                if 0 <= len(data["institutes"]) <= 2:
                    # A User can only be registered in one or two courses; not more.

                    try:
                        institute_one = FpInstitute.objects.get(name=data["institues"][0]["name"],
                                                                semester_half=["institues"][0]["semesterhalf"],
                                                                graduation=["institues"][0]["graduation"],
                                                                registration__semester=semester)
                    except FpInstitute.DoesNotExist:

                        err_data = {"error": "Eines der angegebenen Institute existiert nicht."}
                        return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

                    if data["institutes"][1]:
                        # only do this if a second institute is provided
                        try:
                            institute_two = FpInstitute.objects.get(name=data["institues"][1]["name"],
                                                                    semester_half=["institues"][1]["semesterhalf"],
                                                                    graduation=["institues"][1]["graduation"],
                                                                    registration__semester=semester)
                        except FpInstitute.DoesNotExist:

                            err_data = {"error": "Eines der angegebenen Institute existiert nicht."}
                            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
                    # at this point we now that there is a User, who is real, and all institutes exist wether two or one
                    # next step, check if there is a partner provided and has legit data

                    if data["partner"]:
                        # now we know there is a partner
                        if (data["partner"]["user_firstname"] and data["partner"]["user_firstname"]
                            and data["partner"]["user_login"] and data["partner"]["user_mail"]):
                            # and he has some data provided
                            if il_db_retrieve(user_firstname=data["partner"]["user_firstname"],
                                              user_lastname=data["partner"]["user_lastname"],
                                              user_login=data["partner"]["user_login"],
                                              user_mail=data["partner"]["user_mail"]):
                                # now we know that the Partner is actually registered in the elearning system.
                                if institute_two.places:
                                    if institute_two.places >= 2 and institute_one.places >= 2:
                                        # set the registration

                                        institute_one.places -= 2
                                        institute_two.places -= 2
                                        institute_one.save()
                                        institute_two.save()
                                        try:
                                            partner = FpUserPartner(user_firstname=data["partner"]["user_firstname"],
                                                                    user_lastname=data["partner"]["user_firstname"],
                                                                    user_email=data["partner"]["user_mail"],
                                                                    user_login=data["partner"]["user_login"],
                                                                    institutes=[institute_one, institute_two])

                                            partner.save()
                                        except:
                                            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                        try:
                                            registrant = FpUserRegistrant(user_firstname=data["user_firstname"],
                                                                          user_lastname=data["user_firstname"],
                                                                          user_email=data["user_mail"],
                                                                          user_login=data["user_login"],
                                                                          institutes=[institute_one, institute_two],
                                                                          partner=partner)
                                            registrant.save()
                                        except:
                                            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                                    else:
                                        err_data = {
                                            "error": "In einem der Institute sind nicht mehr ausreichend Plaetze vorhanden."}
                                        return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
                                # if there was no second Institute then register with only one Institute
                                else:
                                    if institute_one.places >= 2:
                                        # set the registration

                                        institute_one.places -= 2
                                        institute_one.save()
                                        try:
                                            partner = FpUserPartner(user_firstname=data["partner"]["user_firstname"],
                                                                    user_lastname=data["partner"]["user_firstname"],
                                                                    user_email=data["partner"]["user_mail"],
                                                                    user_login=data["partner"]["user_login"],
                                                                    institutes=[institute_one, institute_two])

                                            partner.save()
                                        except:
                                            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                        try:
                                            registrant = FpUserRegistrant(user_firstname=data["user_firstname"],
                                                                          user_lastname=data["user_firstname"],
                                                                          user_email=data["user_mail"],
                                                                          user_login=data["user_login"],
                                                                          institutes=[institute_one, institute_two],
                                                                          partner=partner)
                                            registrant.save()
                                        except:
                                            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


                                    else:
                                        err_data = {
                                            "error": "In dem Institut sind nicht mehr ausreichend Plaetze vorhanden."}
                                        return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                err_data = {"error": "Der Partner existiert nicht."}
                                return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

                        else:
                            err_data = {"error": "Die Daten des Partners sind nicht komplett."}
                            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
                    # if there is no partner we obviously only register the user
                    else:
                        if institute_two.places:
                            if institute_two.places >= 1 and institute_one.places >= 1:
                                # set the registration

                                institute_one.places -= 1
                                institute_two.places -= 1
                                institute_one.save()
                                institute_two.save()
                                # no partner
                                try:
                                    registrant = FpUserRegistrant(user_firstname=data["user_firstname"],
                                                                  user_lastname=data["user_firstname"],
                                                                  user_email=data["user_mail"],
                                                                  user_login=data["user_login"],
                                                                  institutes=[institute_one, institute_two])
                                    registrant.save()
                                except:
                                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            else:
                                err_data = {
                                    "error": "In einem der Institute sind nicht mehr ausreichend Plaetze vorhanden."}
                                return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
                        # if there was no second Institute then register with only one Institute
                        else:
                            if institute_one.places >= 1:
                                # set the registration

                                institute_one.places -= 1
                                institute_one.save()
                                try:
                                    registrant = FpUserRegistrant(user_firstname=data["user_firstname"],
                                                                  user_lastname=data["user_firstname"],
                                                                  user_email=data["user_mail"],
                                                                  user_login=data["user_login"],
                                                                  institutes=[institute_one, institute_two])
                                    registrant.save()
                                except:
                                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



                            else:
                                err_data = {
                                    "error": "In dem Institut sind nicht mehr ausreichend Plaetze vorhanden."}
                                return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
                                # registration is set we now retrieve the User and respond the data with a 200 OK status
                    try:
                        user = FpUserRegistrant.objects.get(user_firstname=data["user_firstname"],
                                                            user_lastname=data["user_firstname"],
                                                            user_email=data["user_mail"],
                                                            user_login=data["user_login"],
                                                            institutes=[institute_one, institute_two])
                        serializer = self.get_serializer(data=user)
                    except:
                        err_data = {"error": "Die Anmeldung ist fehlgeschlagen"}
                        return Response(data=err_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    """TODO: send mail to user and(?) partner"""

                    # Registration complete
                    return Response(data=serializer.data, status=status.HTTP_200_OK)

                else:
                    err_data = {"error": "Es wurden mehr als 2 oder gar kein Institut angegeben."}
                    return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                err_data = {"error": "Dieser User existiert nicht."}
                return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        else:
            err_data = {"error": "Die Daten des Registrierenden Users sind nicht vollstaendig."}
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

"""TODO: Add an Accept/Decline partnership View
"""
"""TODO: Add a Cancel Registration view
"""

