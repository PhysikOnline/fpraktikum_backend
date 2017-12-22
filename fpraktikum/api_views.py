# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from fpraktikum.db_utils import il_db_retrieve, check_institute, inst_recover, is_user_valid
from fpraktikum.utils import get_semester, send_email
from .serializers import *


class RegistrationView(ModelViewSet):
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
        login = self.kwargs[self.lookup_field]

        models = {"registrant": (FpUserRegistrant, FpFullUserRegistrantSerializer),
                  "partner": (FpUserPartner, FpFullUserPartnerSerializer),
                  "waitlist": (FpWaitlist, FpWaitlistSerializer),
                  }
        data = {"status": None}
        for k, v in models.items():
            try:
                user = v[0].objects.get(user_login=login)

            except v[0].DoesNotExist:
                pass

            else:

                data = v[1](user).data
                data["status"] = k
        return Response(data)


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


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrantViewset(ModelViewSet):
    """

    This is the main view for registering a Registrant with or without a Partner.
    The PUT method is yet not implemented.
    The DELETE methode will delete the Registrant AND Partner (if Partner has not accepted yet), otherwise the Partner
    will become a Registrant himself.

    """
    name = 'set_registration'
    queryset = FpUserRegistrant.objects.all()
    serializer_class = FpFullUserRegistrantSerializer
    permission_classes = ()

    #for now we do not need a PUT

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.partner_has_accepted:   # if a Partner doesn't exist or hasn't accepted yet delete both
            places = 2 if instance.partner else 1
            for inst in instance.institutes.all():
                inst.places += places
                inst.save()

            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        partner = instance.partner
        # make Partner a Registrant if he already has accepted
        try:
            FpUserRegistrant.create_from_partner(partner)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        for inst in instance.institutes.all():
            inst.places += 1
            inst.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)



    # TODO: "override" the create method using super() and adding a Signal call for emails
    
    # def post(self, request, *args, **kwargs):
    #     """
    #     We rewrite the post command since we don't provide serializer like content.
    #
    #     The request.data dict is expected to look like this :
    #
    #     request.data = {
    #                     'user_firstname': <str>,
    #                     'user_lastname': <str>,
    #                     'user_login': <str>,
    #                     'user_mail': <str>,
    #                     'institutes': [{'name':<str>,
    #                                     'semesterhalf':<int: 1, 2, 3>
    #                                     'graduation':<str: BA, MA, LA>
    #                                     },{...}],
    #                     'partner': {'user_firstname': <str>,
    #                                'user_lastname': <str>,
    #                                'user_login':<str>,
    #                                 'user_mail':<str>,
    #                                },
    #                     }
    #     In this dict the Institutes key should be a list of at least one or two institutes.
    #     Also the partner is optional.
    #
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     data = request.data
    #
    #     serializer = self.serializer_class(data)
    #
    #     if not serializer.is_valid():
    #         return Response(data={'error':serializer.errors },status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer.save()

    # try:
    #     self.serializer_class().run_validation(
    #         data=data)  # This checks if we have the data provided and correct datatypes
    # except ValidationError as err:
    #     return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)
    #
    # # now we know the provided data is ther and has atleast the right Types
    # # check if the User exists
    #
    # if not il_db_retrieve(user_firstname=data["user_firstname"], user_lastname=data["user_lastname"],
    #                       user_login=data["user_login"], user_mail=data["user_mail"],
    #                       user_matrikel=data["user_matrikel"]):
    #     err_data = {"error": "Dieser User existiert nicht im Elearning System"}
    #     return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    # # This checks if the Users Registration status is None
    # if check_user(data["user_login"])["status"]:
    #     err_data = {"error": "Der User hat folgenden Registrierungsstatus :{}".format(
    #         check_user(data["user_login"])["status"])}
    #     return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    # # if a partner is provided we check his status too... for obvious reasons.
    # if data["partner"]:
    #
    #     p_f_name = data["partner"]["user_firstname"]
    #     p_l_name = data["partner"]["user_lastname"]
    #     p_login = data["partner"]["user_login"]
    #     p_mail = data["partner"]["user_mail"]
    #     p_matrikel = data["partner"]["user_matrikel"]
    #
    #     p_status = check_user(data["partner"]["user_login"])["status"]
    #
    #     # Check if Partner is in the ilias System
    #     if not il_db_retrieve(user_firstname=p_f_name, user_lastname=p_l_name,
    #                           user_login=p_login, user_mail=p_mail, user_matrikel=p_mail):
    #         err_data = {"error": "Dieser User existiert nicht im Elearning System"}
    #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    #     # This checks if the partner Registrationstatus is None
    #     if p_status:
    #         err_data = {"error": "Der User hat folgenden Registrierungsstatus :{}".format(p_status)}
    #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    # # now provided user/partner are ready for Registration
    #
    # # check the institutes
    # if len(data["institutes"]) == 2:
    #     # two institutes
    #     try:
    #         institutes = check_institute(institute_one=data["institutes"][0],
    #                                      institute_two=data["institutes"][1])
    #     except FpInstitute.DoesNotExist:
    #         err_data = {"error": "Eins der angegebenen Institute existiert nicht."}
    #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #     # now set registration
    #     if data["partner"]:
    #         if institutes[0].places >= 2 and institutes[1] >= 2:
    #             institutes[0].places -= 2
    #             institutes[1].places -= 2
    #             institutes[0].save()
    #             institutes[1].save()
    #             try:
    #                 user = FpUserRegistrant(user_firstname=data["user_firstname"],
    #                                         user_lastname=data["user_lastname"],
    #                                         user_login=data["user_login"],
    #                                         user_mail=data["user_mail"],
    #                                         user_matrikel=data["user_matrikel"],
    #                                         notes=data["notes"], )
    #                 user.save()
    #                 partner = FpUserPartner(user_firstname=p_f_name,
    #                                         user_lastname=p_l_name,
    #                                         user_login=p_login,
    #                                         user_mail=p_mail,
    #                                         user_matrikel=p_matrikel,
    #                                         registrant=user,
    #                                         notes=data["notes"])
    #                 partner.save()
    #             except (ValueError, IntegrityError) as err:
    #                 inst_recover(institute_one=institutes[0], institute_two=institutes[1], places=2)
    #                 return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #             try:
    #                 user.institutes.set(institutes)
    #                 partner.institutes.set(institutes)
    #             except Exception as err:
    #                 inst_recover(institute_one=institutes[0], institute_two=institutes[1], places=2)
    #                 return Response(data=err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #             # TODO: send mail
    #             # finish with responding the registerd data
    #
    #             send_email(registrant_data={"user_firstname": data["user_firstname"],
    #                                         "user_lastname": data["user_lastname"]},
    #                        partner_data={"user_firstname": p_f_name,
    #                                      "user_lastname": p_l_name},
    #                        registrant_to=data["user_mail"],
    #                        partner_to=p_mail,
    #                        status="reg_reg_2")
    #             serializer = FpFullUserRegistrantSerializer(user)
    #             return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    #         else:
    #             err_data = {"error": u"In einem der ausgewählten Institute ist nicht ausreichend Platz."}
    #             return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    #     else:
    #         # we only register the User
    #         if institutes[0].places >= 1 and institutes[1] >= 1:
    #             institutes[0].places -= 1
    #             institutes[1].places -= 1
    #             institutes[0].save()
    #             institutes[1].save()
    #             try:
    #                 user = FpUserRegistrant(user_firstname=data["user_firstname"],
    #                                         user_lastname=data["user_lastname"],
    #                                         user_login=data["user_login"],
    #                                         user_mail=data["user_mail"],
    #                                         user_matrikel=data["user_matrikel"],
    #                                         notes=data["notes"]
    #                                         )
    #                 user.save()
    #             except (ValueError, IntegrityError) as err:
    #                 inst_recover(institute_one=institutes[0], institute_two=institutes[1], places=2)
    #                 return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #             try:
    #                 user.institutes.set(institutes)
    #             except Exception as err:
    #                 inst_recover(institute_one=institutes[0], institute_two=institutes[1], places=2)
    #                 return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    #             send_email(registrant_data={"user_firstname": data["user_firstname"],
    #                                         "user_lastname": data["user_lastname"]},
    #                        registrant_to=data["user_mail"],
    #                        status="reg_reg_1")
    #             serializer = FpFullUserRegistrantSerializer(user)
    #             return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    #         else:
    #             err_data = {"error": u"In einem der ausgewählten Institute ist nicht ausreichend Platz."}
    #             return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    # else:
    #     # since validation was True we register with one institute
    #     try:
    #         institutes = check_institute(institute_one=data["institutes"][0])
    #     except FpInstitute.DoesNotExist:
    #         err_data = {"error": "Das angegebene Institut existiert nicht."}
    #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #     except ValidationError as err:
    #         return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)
    #
    #     if data["partner"]:
    #         if institutes[0].places >= 2:
    #             institutes[0].places -= 2
    #             institutes[0].save()
    #             try:
    #                 user = FpUserRegistrant(user_firstname=data["user_firstname"],
    #                                         user_lastname=data["user_lastname"],
    #                                         user_login=data["user_login"],
    #                                         user_mail=data["user_mail"],
    #                                         user_matrikel=data["user_matrikel"],
    #                                         notes=data["notes"]
    #                                         )
    #                 user.save()
    #                 partner = FpUserPartner(user_firstname=p_f_name,
    #                                         user_lastname=p_l_name,
    #                                         user_login=p_login,
    #                                         user_mail=p_mail,
    #                                         user_matrikel=p_matrikel,
    #                                         registrant=user,
    #                                         notes=data["notes"]
    #                                         )
    #                 partner.save()
    #             except (ValueError, IntegrityError) as err:
    #                 inst_recover(institute_one=institutes[0], places=1)
    #                 return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #             try:
    #                 user.institutes.set(institutes)
    #                 partner.institutes.set(institutes)
    #             except StandardError as err:
    #                 inst_recover(institute_one=institutes[0], places=1)
    #                 return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    #             send_email(registrant_data={"user_firstname": data["user_firstname"],
    #                                         "user_lastname": data["user_lastname"]},
    #                        partner_data={"user_firstname": p_f_name,
    #                                      "user_lastname": p_l_name},
    #                        registrant_to=data["user_mail"],
    #                        partner_to=p_mail,
    #                        status="reg_reg_2")
    #             serializer = FpFullUserRegistrantSerializer(user)
    #             return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    #         else:
    #             err_data = {"error": u"In einem der ausgewählten Institute ist nicht ausreichend Platz."}
    #             return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         # we only register the user
    #         if institutes[0].places >= 1:
    #             institutes[0].places -= 1
    #             institutes[0].save()
    #             try:
    #                 user = FpUserRegistrant(user_firstname=data["user_firstname"],
    #                                         user_lastname=data["user_lastname"],
    #                                         user_login=data["user_login"],
    #                                         user_mail=data["user_mail"],
    #                                         user_matrikel=data["user_matrikel"],
    #                                         notes=data["notes"]
    #                                         )
    #                 user.save()
    #             except (ValueError, IntegrityError) as err:
    #                 inst_recover(institute_one=institutes[0], places=1)
    #                 return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #             try:
    #                 user.institutes.set(institutes)
    #             except StandardError as err:
    #                 inst_recover(institute_one=institutes[0], places=1)
    #                 return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    #             send_email(registrant_data={"user_firstname": data["user_firstname"],
    #                                         "user_lastname": data["user_lastname"]},
    #                        registrant_to=data["user_mail"],
    #                        status="reg_reg_1")
    #             serializer = FpFullUserRegistrantSerializer(user)
    #             return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    #         else:
    #             err_data = {"error": u"In einem der ausgewählten Institute ist nicht ausreichend Platz."}
    #             return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, *args, **kwargs):
    #     """
    #     Coming soon...
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #
    #     data = request.data
    #
    #     try:
    #         PartnerSerializer().run_validation(data=data)
    #     except ValidationError as err:
    #         return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)
    #     user_status = check_user(login=data["user_login"])["status"]
    #     if not user_status:
    #         err_data = {"error": "Der User ist nicht angemeldet."}
    #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    #     if user_status == "partner":
    #         # we delete the Partner and set the registrant_partner_has_accepted value to Flase
    #         try:
    #             user = FpUserPartner.objects.get(user_firstname=data["user_firstname"],
    #                                              user_lastname=data["user_lastname"],
    #                                              user_login=data["user_login"],
    #                                              user_mail=data["user_mail"],
    #                                              user_matrikel=data["user_matrikel"])
    #         except FpUserPartner.DoesNotExist:
    #             err_data = {"error": "Der User ist nicht angemeldet."}
    #             return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    #         user.registrant.partner_has_accepted = False
    #         user.registrant.save()
    #         try:
    #             institutes = user.institutes.all()
    #             for inst in institutes:
    #                 inst.places += 1
    #                 inst.save()
    #             user.delete()
    #
    #         except:
    #             user.registrant.partner_has_accepted = True
    #             user.registrant.save()
    #             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #         send_email(registrant_data={"user_firstname": user.registrant.user_firstname,
    #                                     "user_lastname": user.registrant.user_lastname},
    #                    partner_data={"user_firstname": data["user_firstname"],
    #                                  "user_lastname": data["user_lastname"]},
    #                    registrant_to=user.registrant.user_mail,
    #                    partner_to=data["user_mail"],
    #                    status="reg_del_partner")
    #         return Response(data={"message": u"Die Anmeldung wurde erfolgreich gelöscht."}, status=status.HTTP_200_OK)
    #
    #     elif user_status == "registrant":
    #         try:
    #             user = FpUserRegistrant.objects.get(user_firstname=data["user_firstname"],
    #                                                 user_lastname=data["user_lastname"],
    #                                                 user_login=data["user_login"],
    #                                                 user_mail=data["user_mail"],
    #                                                 user_matrikel=data["user_matrikel"])
    #
    #         except FpUserRegistrant.DoesNotExist:
    #             err_data = {"error": "Der User ist nicht angemeldet."}
    #             return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #         try:
    #             partner = user.partner
    #         except FpUserRegistrant.partner.RelatedObjectDoesNotExist:
    #             partner = None
    #         if partner and user.partner_has_accepted:
    #             # get the Partner Data and make him a Registrant
    #             # partner_as_registrant = FpUserRegistrant.create_from_partner(user)
    #             try:
    #                 FpUserRegistrant.create_from_partner(user.partner)
    #             except IntegrityError as err:
    #                 return Response(data=err.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    #             try:
    #                 institutes = user.institutes.all()
    #                 for inst in institutes:
    #                     inst.places += 1
    #                     inst.save()
    #                 user.delete()
    #             except:
    #                 return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #             send_email(registrant_data={"user_firstname": data["user_firstname"],
    #                                         "user_lastname": data["user_firstname"]},
    #                        partner_data={"user_firstname": user.partner.user_firstname,
    #                                      "user_lastname": user.partner.user_lastname},
    #                        registrant_to=data["user_mail"],
    #                        partner_to=user.partner.user_mail,
    #                        status="reg_del_partner_stays")
    #             return Response(data={"message": u"Die Anmeldung wurde erfolgreich gelöscht."},
    #                             status=status.HTTP_200_OK)
    #             # elif user.partner and not user.partner_has_accepted:
    #             # has partner but did not accept yet. Delete both.
    #
    #         else:
    #             # here we actually deal with two cases:
    #             # 1. He has a partner but the partner did not accept yet --> delete both add 2 to institutes.places
    #             # 2. He has no partner --> delete him add 1 to institutes.places
    #
    #             places = 2 if partner else 1
    #
    #             try:
    #                 institutes = user.institutes.all()
    #                 for inst in institutes:
    #                     inst.places += places
    #                     inst.save()
    #
    #                 user.delete()
    #
    #             except:
    #                 return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #             if partner:
    #                 send_email(registrant_data={"user_firstname": data["user_firstname"],
    #                                             "user_lastname": data["user_lastname"]},
    #                            partner_data={"user_firstname": user.partner.user_firstname,
    #                                          "user_lastname": user.partner.user_lastname},
    #                            registrant_to=data["user_mail"],
    #                            partner_to=user.partner.user_mail,
    #                            status="reg_del_2")
    #             else:
    #                 send_email(registrant_data={"user_firstname": data["user_firstname"],
    #                                             "user_lastname": data["user_lastname"]},
    #                            registrant_to=data["user_mail"],
    #                            status="reg_del_1")
    #             return Response(data={"message": u"Die Anmeldung wurde erfolgreich gelöscht."},
    #                             status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UserPartnerViewset(ModelViewSet):
    name = 'accept'
    queryset = FpUserPartner.objects.all()
    serializer_class = FpFullUserPartnerSerializer
    permission_classes = ()

    def update(self, request, *args, **kwargs):
        """
        This method is used to Accept the so called Partnership.
        In the future we might want to be reutilize this methode for more update possibilities.
        Yet it's kind of static.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer_class()
        instance = self.get_object()
        # set the accept
        instance.has_accepted = True
        instance.save()
        instance.registrant.partner_has_accepted = True
        instance.registrant.save()

        return Response(data=serializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for inst in instance.institutes.all():
            inst.places += 1
            inst.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
    # def post(self, request, *args, **kwargs):
    #     """
    #     Docstring coming soon...
    #
    #     request.data = {    # partner data
    #                     'user_firstname': <str>,
    #                     'user_lastname': <str>,
    #                     'user_login': <str>,
    #                     'user_mail': <str>,
    #                     'user_matrikel': <str>
    #                     'accept':<boolean> # True for accept , False for decline
    #                     }
    #
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     data = request.data
    #
    #     # validate data
    #     try:
    #         self.serializer_class().run_validation(data)
    #     except ValidationError as err:
    #         return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)
    #
    #     # check if User is a registered Partner
    #
    #     try:
    #         partner = FpUserPartner.objects.get(user_firstname=data["user_firstname"],
    #                                             user_lastname=data["user_lastname"],
    #                                             user_login=data["user_login"],
    #                                             user_mail=data["user_mail"],
    #                                             user_matrikel=data["user_matrikel"])
    #
    #     except FpUserPartner.DoesNotExist:
    #         err_data = {"error": "Der user ist kein eingetragener Partner."}
    #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    #     if data["accept"]:
    #         try:
    #             partner.has_accepted = True
    #             partner.save()
    #             partner.registrant.partner_has_accepted = True
    #             partner.registrant.save()
    #         except ValueError as err:
    #             return Response(data=err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #         send_email(registrant_data={"user_firstname": partner.registrant.user_firstname,
    #                                     "user_lastname": partner.registrant.user_lastname},
    #                    partner_data={"user_firstname": data["user_firstname"],
    #                                  "user_lastname": data["user_lastname"],
    #                                  "registrant_firstname": partner.registrant.user_firstname,
    #                                  "registrant_lastname": partner.registrant.user_lastname},
    #                    registrant_to=partner.registrant.user_mail,
    #                    partner_to=data["user_mail"],
    #                    status="accept_acc")
    #         return Response(status=status.HTTP_200_OK)
    #
    #     # delete The partner
    #     else:
    #         try:
    #             partner.delete()
    #         except Exception as err:
    #             return Response(data=err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #         send_email(registrant_data={"user_firstname": partner.registrant.user_firstname,
    #                                     "user_lastname": partner.registrant.user_lastname},
    #                    partner_data={"user_firstname": data["user_firstname"],
    #                                  "user_lastname": data["user_lastname"],
    #                                  "registrant_firstname": partner.registrant.user_firstname,
    #                                  "registrant_lastname": partner.registrant.user_lastname},
    #                    registrant_to=partner.registrant.user_mail,
    #                    partner_to=data["user_mail"],
    #                    status="accept_dec")
    #         return Response(status=status.HTTP_200_OK)


#this is already covered in the rewritten UserCheckView
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
            return Response(status=status.HTTP_200_OK)

        check = is_user_valid(login=data["user_login"])

        if check["status"]:
            resp_data = check["data"]
            resp_data["status"] = check["status"]
            return Response(data=resp_data, status=status.HTTP_200_OK)

        else:
            resp_data = partner_data
            resp_data["status"] = check["status"]
            return Response(data=resp_data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class WaitlistView(ModelViewSet):
    name = "waitlist"
    serializer_class = FpWaitlistSerializer
    queryset = FpWaitlist.objects.all()
    permission_classes = ()

    # def post(self, request, *args, **kwargs):
    #
    #     data = request.data
    #     # TODO : This Code block (till the next try statement) occurs more often as Copy_Paste. Refactor it in a function!
    #
    #     try:
    #         self.serializer_class().run_validation(data=data)
    #     except ValidationError as err:
    #         return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)
    #
    #     if not il_db_retrieve(user_firstname=data["user_firstname"], user_lastname=data["user_lastname"],
    #                           user_login=data["user_login"], user_mail=data["user_mail"],
    #                           user_matrikel=data["user_matrikel"]):
    #         err_data = {"error": "Dieser User existiert nicht im Elearning System"}
    #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    #     if check_user(data["user_login"])["status"]:
    #         err_data = {
    #             "error": "Der User hat folgenden Registrierungsstatus :{}".format(
    #                 check_user(data["user_login"])["status"])}
    #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #
    #     # everything fine set waitlist entry
    #
    #     try:
    #         user = FpWaitlist(user_firstname=data["user_firstname"],
    #                           user_lastname=data["user_lastname"],
    #                           user_login=data["user_login"],
    #                           user_mail=data["user_mail"],
    #                           user_matrikel=data["user_matrikel"],
    #                           graduation=data["graduation"],
    #                           notes=data["notes"]
    #                           )
    #         user.save()
    #     except Exception:
    #         return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     send_email(registrant_data={"user_firstname": data["user_firstname"],
    #                                 "user_lastname": data["user_lastname"]},
    #                registrant_to=data["user_mail"],
    #                status="waitlist_reg")
    #     return_data = FpWaitlistSerializer(user)
    #     return Response(data=return_data.data, status=status.HTTP_200_OK)
    #
    # def delete(self, request, *args, **kwargs):
    #
    #     data = request.data
    #
    #     try:
    #         self.serializer_class().run_validation(data=data)
    #     except ValidationError as err:
    #         return Response(data=err.detail, status=status.HTTP_400_BAD_REQUEST)
    #
    #     try:
    #         user = FpWaitlist.objects.get(user_firstname=data["user_firstname"],
    #                                       user_lastname=data["user_lastname"],
    #                                       user_login=data["user_login"],
    #                                       user_mail=data["user_mail"],
    #                                       user_matrikel=data["user_matrikel"])
    #     except FpWaitlist.DoesNotExist:
    #         err_data = {"error": "Der User steht nicht auf der Warteliste."}
    #         return Response(data=err_data, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         user.delete()
    #     except:
    #         return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     send_email(registrant_data={"user_firstname": data["user_firstname"],
    #                                 "user_lastname": data["user_lastname"]},
    #                registrant_to=data["user_mail"],
    #                status="waitlist_del")
    #     return Response(status=status.HTTP_200_OK)
