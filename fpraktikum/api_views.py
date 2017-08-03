from rest_framework import generics
from .models import *
from .serializers import *
from .utils import get_semester
from django.shortcuts import get_object_or_404

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


