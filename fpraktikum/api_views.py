# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.request import HttpRequest
from django.urls import reverse
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from rest_framework.permissions import IsAdminUser, IsAuthenticated
from auth_backends.auth import UserBackend, AdminBackend
from auth_backends.permissions import OnlyAdminGet, OnlyAdminPostDelete
from fpraktikum.admin import RegistrantResource, WaitlistResource

from fpraktikum.utils import get_semester, send_email

from .serializers import *
from fpraktikum.views import ExportView


class RegistrationView(ModelViewSet):
    name = 'registration'
    queryset = FpRegistration.objects.all()
    serializer_class = FpRegistrationSerializer
    authentication_classes = (UserBackend, AdminBackend)
    permission_classes = (OnlyAdminPostDelete,)


class CurrentRegistrationView(generics.RetrieveAPIView):
    name = 'current-registration'
    queryset = FpRegistration.objects.all()
    serializer_class = FpRegistrationSerializer
    authentication_classes = (UserBackend, AdminBackend)
    permission_classes = (OnlyAdminPostDelete,)

    def get_object(self):
        current_semester = get_semester()
        obj = self.get_queryset().filter(semester=current_semester)
        obj = get_object_or_404(obj)
        return obj


class UserCheckView(generics.RetrieveAPIView):
    name = 'user'
    lookup_field = 'user_login'
    serializer_class = DummySerializer
    queryset = FpUserRegistrant.objects.all()
    authentication_classes = (UserBackend, AdminBackend)
    permission_classes = (IsAuthenticated,)
    models = {"registrant": (FpUserRegistrant, FpFullUserRegistrantSerializer),
              "partner": (FpUserPartner, FpFullUserPartnerSerializer),
              "waitlist": (FpWaitlist, FpWaitlistSerializer),
              }

    def get_models(self):
        return self.models

    def get_login(self):
        return self.kwargs[self.lookup_field]

    def get_response_data(self, login):
        login = login

        models = self.get_models()
        data = {"status": None}
        for k, v in models.items():
            try:
                user = v[0].objects.get(user_login=login)

            except v[0].DoesNotExist:
                pass

            else:

                data = v[1](user).data
                data["status"] = k
        return data

    def get(self, request, *args, **kwargs):
        """
        Returns the object the view is displaying.
        """
        login = self.get_login()
        data = self.get_response_data(login)
        return Response(data)

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
    authentication_classes = (UserBackend, AdminBackend)
    permission_classes = (OnlyAdminGet,)

    def perform_create(self, serializer):
        user = serializer.save()
        send_email(user, "reg_reg")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.partner_has_accepted:   # if a Partner doesn't exist or hasn't accepted yet delete both

            try:
                instance.partner
            except FpUserPartner.DoesNotExist:
                places = 1
            else:
                places = 2

            for inst in instance.institutes.all():
                inst.places += places
                inst.save()
            send_email(instance, "reg_del")
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
        send_email(instance, "reg_del_partner_stays")
        return Response(status=status.HTTP_204_NO_CONTENT)

    # for now we do not need a PUT

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)



@method_decorator(csrf_exempt, name='dispatch')
class UserPartnerViewset(ModelViewSet):
    name = 'accept'
    queryset = FpUserPartner.objects.all()
    serializer_class = FpFullUserPartnerSerializer
    authentication_classes = (UserBackend, AdminBackend)
    permission_classes = (OnlyAdminGet,)

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

        send_email(instance.registrant, "accept_acc")
        return Response(data=serializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        """
        This method is used to Decline a Partnership or to delete a Partner.


        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        mail_str ="accept_dec"  # we use a mail_string since this method
                                # will also be called when declineing the Partnership

        if instance.has_accepted:
            instance.registrant.partner_has_accepted = False
            instance.registrant.save()
            mail_str = "reg_del_partner"

        for inst in instance.institutes.all():
            inst.places += 1
            inst.save()

        self.perform_destroy(instance)
        send_email(instance.registrant, mail_str)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class CheckPartnerView(UserCheckView):
    name = "check_partner"

    serializer_class = DummySerializer
    queryset = FpUserPartner.objects.all()
    authentication_classes = (UserBackend, AdminBackend)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        login = request.query_params.get("user_login")
        last_name = request.query_params.get("user_lastname")

        serializer = self.get_serializer()

        user_legal = il_db_retrieve(user_lastname=last_name, user_login=login)  # will store the needed data or None

        if not user_legal:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # we retrive the usual "CheckUser data"
        data = self.get_response_data(login)

        if not data["status"]:  # if status is None the User isn' registered so we provide the Data
            return Response(user_legal)

        return Response(data)


@method_decorator(csrf_exempt, name='dispatch')
class WaitlistView(ModelViewSet):
    name = "waitlist"
    serializer_class = FpWaitlistSerializer
    queryset = FpWaitlist.objects.all()
    authentication_classes = (UserBackend, AdminBackend)
    permission_classes = (OnlyAdminGet,)

    def perform_create(self, serializer):
        user = serializer.save()
        send_email(user, "waitlist_reg")

    def perform_destroy(self, instance):
        send_email(instance, "waitlist_del")
        instance.delete()

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class ExportRegistrantsView(ExportView):

    queryset = FpUserRegistrant.objects.all()
    serializer_class = DummySerializer
    permission_classes = (IsAuthenticated,)     # The View is yet not used and therefore could be abused
    resource_class = RegistrantResource
    file_name = "Registrants"


class ExportWaitlistView(ExportView):
    queryset = FpWaitlist.objects.all()
    serializer_class = DummySerializer
    permission_classes = (IsAuthenticated,)     # The View is yet not used and therefore could be abused
    resource_class = WaitlistResource
    file_name = "Waitlist"


