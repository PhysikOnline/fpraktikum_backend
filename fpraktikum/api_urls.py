from django.conf.urls import url
from django.contrib import admin
from .api_views import *

app_name = "api"
urlpatterns = [
    url(r'^registration', RegistrationView.as_view(), name=RegistrationView.name),
]