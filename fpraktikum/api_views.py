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
    lookup_field = 'user_snumber'
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

        is_registrant = FpUserRegistrant.objects.filter(user_snumber=self.kwargs[lookup_field],
                                                        institutes__registration__semester=semester)
        is_partner = FpUserPartner.objects.filter(user_snumber=self.kwargs[lookup_field],
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

