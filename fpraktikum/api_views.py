# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from braces.views import CsrfExemptMixin

from fpraktikum.db_utils import il_db_retrieve, check_user, check_institute, inst_recover
from fpraktikum.utils import get_semester
from .serializers import *


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

        user_status_data = check_user(self.kwargs[lookup_field])
        response_data = user_status_data["data"]
        response = Response(response_data)
        response.data["status"] = user_status_data["status"]
        return response

        # is_registrant = FpUserRegistrant.objects.filter(user_login=self.kwargs[lookup_field],
        #                                                 institutes__registration__semester=semester)
        # is_partner = FpUserPartner.objects.filter(user_login=self.kwargs[lookup_field],
        #                                           institutes__registration__semester=semester)
        # if is_registrant:
        #     obj = is_registrant.distinct(lookup_field).get()
        #     serializer = FpFullUserRegistrantSerializer(obj)
        #     response = Response(serializer.data)
        #     response.data["status"] = "registrant"
        #     return response
        #
        # elif is_partner:
        #     obj = is_partner.distinct(lookup_field).get()
        #     serializer = FpFullUserPartnerSerializer(obj)
        #     response = Response(serializer.data)
        #     response.data["status"] = "partner"
        #     return response
        # else:
        #     data = {"status": None}
        #     return Response(data)

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


# TODO Think about checking inst_one == inst_two and wether User/Partner is allready registered.

class SetRegistrationView(CsrfExemptMixin, views.APIView):
    """
    This is the main view for setting a Registration to the Fortgeschrittenen Praktikum.

    """
    name = 'set_registration'
    queryset = FpUserRegistrant.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        We rewrite the post command since we don't provide serializer like content.

        The request.data dict is expected to look like this :

        request.data = {
                        'user_firstname': <str>,
                        'user_lastname': <str>,
                        'user_login': <str>,
                        'user_mail': <str>,
                        'institutes': [{'name':<str>,
                                        'semesterhalf':<int: 1, 2, 3>
                                        'graduation':<str: BA, MA, LA>
                                        },{...}],
                        'partner': {'user_firstname': <str>,
                                   'user_lastname': <str>,
                                   'user_login':<str>,
                                    'user_mail':<str>,
                                   },
                        }
        In this dict the Institutes key should be a list of at least one or two institutes.
        Also the partner is optional.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data

        semester = get_semester()

        try:
            self.serializer_class().run_validation(data=data)    # This checks if we have the data provided and correct datatypes
        except ValidationError as err:
            return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)

        # now we know the provided data is ther and has atleast the right Types
        # check if the User exists

        if not il_db_retrieve(user_firstname=data["user_firstname"], user_lastname=data["user_lastname"],
                              user_login=data["user_login"], user_mail=data["user_mail"],
                              user_matrikel=data["user_matrikel"]):

            err_data = {"error": "Dieser User existiert nicht im Elearning System"}
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        # This checks if the Users Registration status is None
        if check_user(data["user_login"])["status"]:
            err_data = {"error": "Der User hat folgenden Registrierungsstatus :{}".format(check_user(data["user_login"])["status"])}
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        # if a partner is provided we check his status too... for obvious reasons.
        if data["partner"]:

            p_f_name = data["partner"]["user_firstname"]
            p_l_name = data["partner"]["user_lastname"]
            p_login = data["partner"]["user_login"]
            p_mail = data["partner"]["user_mail"]
            p_matrikel = data["partner"]["user_matrikel"]

            with check_user(data["partner"]["user_login"])["status"] as p_status:

                # Check if Partner is in the ilias System
                if not il_db_retrieve(user_firstname=p_f_name, user_lastname=p_l_name,
                                      user_login=p_login,user_mail=p_mail, user_matrikel=p_mail):
                    err_data = {"error": "Dieser User existiert nicht im Elearning System"}
                    return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

                # This checks if the partner Registrationstatus is None
                if p_status:
                    err_data = {"error": "Der User hat folgenden Registrierungsstatus :{}".format(p_status)}
                    return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        # now provided user/partner are ready for Registration

        # check the institutes
        if len(data["institutes"]) == 2:
            # two institutes
            try:
                institutes = check_institute(institute_one=data["institutes"][0],
                                             institute_two=data["institutes"][1])
            except FpInstitute.DoesNotExist:
                err_data = {"error": "Eins der angegebenen Institute existiert nicht."}
                return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
            # now set registration
            if data["partner"]:
                if institutes[0].places >= 2 and institutes[1] >= 2:
                    institutes[0].places -= 2
                    institutes[1].places -= 2
                    institutes[0].save()
                    institutes[1].save()
                    try:
                        user = FpUserRegistrant(user_firstname=data["user_firstname"],
                                                user_lastname=data["user_lastname"],
                                                user_login=data["user_login"],
                                                user_email=data["user_mail"],
                                                user_matrikel=data["user_matrikel"])
                        user.save()
                        partner = FpUserPartner(user_firstname=p_f_name,
                                                user_lastname=p_l_name,
                                                user_login=p_login,
                                                user_email=p_mail,
                                                user_matrikel=p_matrikel,
                                                registrant=user)
                        partner.save()
                    except (ValueError, IntegrityError) as err:
                        inst_recover(institute_one=institutes[0], institute_two=institutes[1], places=2)
                        return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    try:
                        user.institutes.set(institutes)
                        partner.institutes.set(institutes)
                    except Exception as err:
                        inst_recover(institute_one=institutes[0], institute_two=institutes[1], places=2)
                        return Response(data=err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    # TODO: send mail
                    # finish with responding the registerd data

                    serializer = FpFullUserRegistrantSerializer(user)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)

                else:
                    err_data = {"error": u"In einem der ausgewählten Institute ist nicht ausreichend Platz."}
                    return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

            else:
                # we only register the User
                if institutes[0].places >= 1 and institutes[1] >= 1:
                    institutes[0].places -= 1
                    institutes[1].places -= 1
                    institutes[0].save()
                    institutes[1].save()
                    try:
                        user = FpUserRegistrant(user_firstname=data["user_firstname"],
                                                user_lastname=data["user_lastname"],
                                                user_login=data["user_login"],
                                                user_email=data["user_mail"],
                                                user_matrikel=data["user_matrikel"])
                        user.save()
                    except (ValueError, IntegrityError) as err:
                        inst_recover(institute_one=institutes[0], institute_two=institutes[1], places=2)
                        return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    try:
                        user.institutes.set(institutes)
                    except Exception as err:
                        inst_recover(institute_one=institutes[0], institute_two=institutes[1], places=2)
                        return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    serializer = FpFullUserRegistrantSerializer(user)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)

                else:
                    err_data = {"error": u"In einem der ausgewählten Institute ist nicht ausreichend Platz."}
                    return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        else:
            # since validation was True we register with one institute
            try:
                institutes = check_institute(institute_one=data["institutes"][0])
            except FpInstitute.DoesNotExist:
                err_data = {"error": "Das angegebene Institut existiert nicht."}
                return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as err:
                return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)

            if data["partner"]:
                if institutes[0].places >= 2:
                    institutes[0].places -= 2
                    institutes[0].save()
                    try:
                        user = FpUserRegistrant(user_firstname=data["user_firstname"],
                                                user_lastname=data["user_lastname"],
                                                user_login=data["user_login"],
                                                user_email=data["user_mail"],
                                                user_matrikel=data["user_matrikel"])
                        user.save()
                        partner = FpUserPartner(user_firstname=p_f_name,
                                                user_lastname=p_l_name,
                                                user_login=p_login,
                                                user_email=p_mail,
                                                user_matrikel=p_matrikel,
                                                registrant=user)
                        partner.save()
                    except (ValueError, IntegrityError) as err:
                        inst_recover(institute_one=institutes[0], places=1)
                        return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    try:
                        user.institutes.set(institutes)
                        partner.institutes.set(institutes)
                    except StandardError as err:
                        inst_recover(institute_one=institutes[0], places=1)
                        return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    serializer = FpFullUserRegistrantSerializer(user)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)

                else:
                    err_data = {"error": u"In einem der ausgewählten Institute ist nicht ausreichend Platz."}
                    return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                # we only register the user
                if institutes[0].places >= 1:
                    institutes[0].places -= 1
                    institutes[0].save()
                    try:
                        user = FpUserRegistrant(user_firstname=data["user_firstname"],
                                                user_lastname=data["user_lastname"],
                                                user_login=data["user_login"],
                                                user_email=data["user_mail"],
                                                user_matrikel=data["user_matrikel"])
                        user.save()
                    except (ValueError, IntegrityError) as err:
                        inst_recover(institute_one=institutes[0], places=1)
                        return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    try:
                        user.institutes.set(institutes)
                    except StandardError as err:
                        inst_recover(institute_one=institutes[0], places=1)
                        return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    serializer = FpFullUserRegistrantSerializer(user)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)

                else:
                    err_data = {"error": u"In einem der ausgewählten Institute ist nicht ausreichend Platz."}
                    return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

 # validate

        # if data["user_firstname"] and data["user_lastname"] and data["user_login"] and data["user_mail"]:
        #     # we want to be sure that this data is atleast provided
        #     if il_db_retrieve(user_firstname=data["user_firstname"], user_lastname=data["user_lastname"],
        #                       user_login=data["user_login"], user_mail=data["user_mail"]):
        #         # we want to know if this user actually exists in the elearning system
        #
        #         if 0 <= len(data["institutes"]) <= 2:
        #             # A User can only be registered in one or two courses; not more.
        #
        #             try:
        #                 institute_one = FpInstitute.objects.get(name=data["institutes"][0]["name"],
        #                                                         semester_half=data["institutes"][0]["semesterhalf"],
        #                                                         graduation=data["institutes"][0]["graduation"],
        #                                                         registration__semester=semester)
        #             except FpInstitute.DoesNotExist:
        #
        #                 err_data = {"error": "Eines der angegebenen Institute existiert nicht."}
        #                 return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #
        #             if data["institutes"][1]:
        #                 # only do this if a second institute is provided
        #                 try:
        #                     institute_two = FpInstitute.objects.get(name=data["institutes"][1]["name"],
        #                                                             semester_half=data["institutes"][1]["semesterhalf"],
        #                                                             graduation=data["institutes"][1]["graduation"],
        #                                                             registration__semester=semester)
        #                 except FpInstitute.DoesNotExist:
        #
        #                     err_data = {"error": "Eines der angegebenen Institute existiert nicht."}
        #                     return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #             # at this point we now that there is a User, who is real, and all institutes exist wether two or one
        #             # next step, check if there is a partner provided and has legit data
        #
        #             if data["partner"]:
        #                 # now we know there is a partner
        #                 if (data["partner"]["user_firstname"] and data["partner"]["user_lastname"]
        #                         and data["partner"]["user_login"] and data["partner"]["user_mail"]):
        #                     # and he has some data provided
        #                     if il_db_retrieve(user_firstname=data["partner"]["user_firstname"],
        #                                       user_lastname=data["partner"]["user_lastname"],
        #                                       user_login=data["partner"]["user_login"],
        #                                       user_mail=data["partner"]["user_mail"]):
        #                         # now we know that the Partner is actually registered in the elearning system.
        #                         if institute_two.places:
        #                             if institute_two.places >= 2 and institute_one.places >= 2:
        #                                 # set the registration
        #                                 # We want to reduce the places before hand due to the fact that someone else
        #                                 # might register with the same set a bit later ...
        #                                 institute_one.places -= 2
        #                                 institute_two.places -= 2
        #                                 institute_one.save()
        #                                 institute_two.save()
        #                                 try:
        #                                     registrant = FpUserRegistrant(user_firstname=data["user_firstname"],
        #                                                                   user_lastname=data["user_lastname"],
        #                                                                   user_email=data["user_mail"],
        #                                                                   user_login=data["user_login"],
        #                                                                   )
        #                                     registrant.save()
        #                                     registrant.institutes.set([institute_one, institute_two])
        #                                 except:
        #
        #                                     #TODO: Over think smth like this to not take away places when an exception
        #                                     #got thrown.
        #
        #                                     # institute_one.places -= 2
        #                                     # institute_two.places -= 2
        #                                     # institute_one.save()
        #                                     # institute_two.save()
        #                                     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        #                                 try:
        #                                     partner = FpUserPartner(user_firstname=data["partner"]["user_firstname"],
        #                                                             user_lastname=data["partner"]["user_lastname"],
        #                                                             user_email=data["partner"]["user_mail"],
        #                                                             user_login=data["partner"]["user_login"],
        #                                                             registrant=registrant)
        #
        #                                     partner.save()
        #                                     partner.institutes.set([institute_one, institute_two])
        #                                 except:
        #                                     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        #                             else:
        #                                 err_data = {
        #                                     "error": "In einem der Institute sind nicht mehr ausreichend Plaetze vorhanden."}
        #                                 return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #                         # if there was no second Institute then register with only one Institute
        #                         else:
        #                             if institute_one.places >= 2:
        #                                 # set the registration
        #
        #                                 institute_one.places -= 2
        #                                 institute_one.save()
        #                                 try:
        #                                     registrant = FpUserRegistrant(user_firstname=data["user_firstname"],
        #                                                                   user_lastname=data["user_lastname"],
        #                                                                   user_email=data["user_mail"],
        #                                                                   user_login=data["user_login"],)
        #                                     registrant.save()
        #                                     registrant.institutes.set([institute_one,])
        #                                 except:
        #                                     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        #                                 try:
        #                                     partner = FpUserPartner(user_firstname=data["partner"]["user_firstname"],
        #                                                             user_lastname=data["partner"]["user_lastname"],
        #                                                             user_email=data["partner"]["user_mail"],
        #                                                             user_login=data["partner"]["user_login"],
        #                                                             registrant=registrant)
        #
        #                                     partner.save()
        #                                     partner.institutes.set([institute_one, ])
        #                                 except:
        #                                     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        #                             else:
        #                                 err_data = {
        #                                     "error": "In dem Institut sind nicht mehr ausreichend Plaetze vorhanden."}
        #                                 return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #                     else:
        #                         err_data = {"error": "Der Partner existiert nicht."}
        #                         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #
        #                 else:
        #                     err_data = {"error": "Die Daten des Partners sind nicht komplett."}
        #                     return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #             # if there is no partner we obviously only register the user
        #             else:
        #                 if institute_two.places:
        #                     if institute_two.places >= 1 and institute_one.places >= 1:
        #                         # set the registration
        #
        #                         institute_one.places -= 1
        #                         institute_two.places -= 1
        #                         institute_one.save()
        #                         institute_two.save()
        #                         # no partner
        #                         try:
        #                             registrant = FpUserRegistrant(user_firstname=data["user_firstname"],
        #                                                           user_lastname=data["user_lastname"],
        #                                                           user_email=data["user_mail"],
        #                                                           user_login=data["user_login"],
        #                                                           )
        #                             registrant.save()
        #                             registrant.institutes.set([institute_one, institute_two])
        #                         except:
        #                             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        #                     else:
        #                         err_data = {
        #                             "error": "In einem der Institute sind nicht mehr ausreichend Plaetze vorhanden."}
        #                         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #                 # if there was no second Institute then register with only one Institute
        #                 else:
        #                     if institute_one.places >= 1:
        #                         # set the registration
        #
        #                         institute_one.places -= 1
        #                         institute_one.save()
        #                         try:
        #                             registrant = FpUserRegistrant(user_firstname=data["user_firstname"],
        #                                                           user_lastname=data["user_lastname"],
        #                                                           user_email=data["user_mail"],
        #                                                           user_login=data["user_login"],
        #                                                           )
        #                             registrant.save()
        #                             registrant.institutes.set([institute_one, ])
        #                         except:
        #                             err_data = {"error": "here"}
        #                             return Response(data=err_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        #
        #
        #                     else:
        #                         err_data = {
        #                             "error": "In dem Institut sind nicht mehr ausreichend Plaetze vorhanden."}
        #                         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #                         # registration is set we now retrieve the User and respond the data with a 200 OK status
        #             try:
        #                 user = FpUserRegistrant.objects.get(user_firstname=data["user_firstname"],
        #                                                     user_lastname=data["user_lastname"],
        #                                                     user_email=data["user_mail"],
        #                                                     user_login=data["user_login"],
        #                                                     )
        #                 serializer = FpFullUserRegistrantSerializer(user)
        #             except:
        #                 err_data = {"error": "Die Anmeldung ist fehlgeschlagen"}
        #                 return Response(data=err_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #             #TODO: send mail to user and(?) partner
        #
        #             # Registration complete
        #             return Response(data=serializer.data, status=status.HTTP_200_OK)
        #
        #         else:
        #             err_data = {"error": "Es wurden mehr als 2 oder gar kein Institut angegeben."}
        #             return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #     else:
        #         err_data = {"error": "Dieser User existiert nicht."}
        #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #
        # else:
        #     err_data = {"error": "Die Daten des Registrierenden Users sind nicht vollstaendig."}
        #     return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
        #this is the old version


class AcceptDeclinePartnershipView(generics.CreateAPIView):
    name = 'accept'
    queryset = FpUserPartner.objects.all()
    serializer_class = AcceptDeclineSerializer

    def post(self, request, *args, **kwargs):
        """
        Docstring coming soon...

        request.data = {    # partner data
                        'user_firstname': <str>,
                        'user_lastname': <str>,
                        'user_login': <str>,
                        'user_mail': <str>,
                        'user_matrikel': <str>
                        'accept':<boolean> # True for accept , False for decline
                        }

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data

        # validate data
        try:
            self.serializer_class().run_validation(data)
        except ValidationError as err:
            return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)

        # check if User is a registered Partner

        try:
            partner = FpUserPartner.objects.get(user_firstname=data["user_firstname"],
                                                user_lastname=data["user_lastname"],
                                                user_login=data["user_login"],
                                                user_email=data["user_mail"],
                                                user_matrikel=data["user_matrikel"])

        except FpUserPartner.DoesNotExist:
            err_data = {"error": "Der user ist kein eingetragener Partner."}
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        if data["accept"]:
            try:
                partner.has_accepted = True
                partner.save()
                partner.registrant.partner_has_accepted = True
                partner.registrant.save()
            except ValueError as err:
                return Response(data=err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(status=status.HTTP_200_OK)

        # delete The partner
        else:
            try:
                partner.delete()
            except Exception as err:
                return Response(data=err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(status=status.HTTP_200_OK)


            # first check if the data is even provided
            #
            # if data['user_firstname'] and data['user_lastname'] and data['user_login'] and data['user_mail']:
            #     # ok data is provided
            #     # let's check if the user is really a "registered" Partner
            #     try:
            #         partner_data = FpUserPartner.objects.get(user_firstname=data['user_firstname'],
            #                                                  user_lastname=data['user_lastname'],
            #                                                  user_login=data['user_login'],
            #                                                  user_email=data['user_mail'])
            #     except FpUserPartner.DoesNotExist:
            #         err_data = {"error": "Der User ist kein eingetragener Partner."}
            #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
            #
            #     if data["accept_decline"]:
            #         # partner accepts
            #         partner_data.has_accepted = True
            #         partner_data.registrant.partner_has_accepted = True
            #         try:
            #             partner_data.save()
            #             partner_data.registrant.save()
            #
            #         except:
            #             err_data = {"error": "Der Prozess ist fehlgeschlagen."}
            #             return Response(data=err_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            #     else:
            #         # Partner declines so we delete him
            #         try:
            #
            #             partner_data.delete()
            #
            #         except:
            #             err_data = {"error": "Der Prozess ist fehlgeschlagen."}
            #             return Response(data=err_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            #
            #     return Response(status=status.HTTP_200_OK)
            #
            #
            #
            # else:
            #     err_data = {"error": "Die Daten des Users sind nicht vollstaendig."}
            #     return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)


class CheckPartnerView(views.APIView):
    name = "check_partner"
    serializer_class = CheckPartnerSerializer
    queryset = FpUserPartner.objects.all()

    def get(self, request, *args, **kwargs):

        data = request.GET
        resp_data = {}
        try:

            self.serializer_class().run_validation(data=data)

        except ValidationError as err:
            return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)

        partner_data = il_db_retrieve(user_lastname=data["user_lastname"], user_login=data["user_login"])

        if not partner_data:
            err_data = {"error": "Dieser User existiert nicht im Elearning System."}
            return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

        check = check_user(login=data["user_login"])

        if check["status"]:
            resp_data = check["data"]
            resp_data["status"] = check["status"]
            return Response(data=resp_data,status=status.HTTP_400_BAD_REQUEST)       # which status ?

        else:
            resp_data = partner_data
            resp_data["status"] = check["status"]
            return Response(data=resp_data, status=status.HTTP_200_OK)



class CancelRegistrationView():
    pass
#TODO: Add a Cancel Registration view


