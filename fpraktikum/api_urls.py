from django.conf.urls import url

from fpraktikum.api_views import *

app_name = "api"
urlpatterns = [
    url(r'^registration/', RegistrationView.as_view(), name=RegistrationView.name),
    url(r'^user/(?P<user_snumber>.+)/', UserCheckView.as_view(), name=UserCheckView.name),
    url(r'^user/register/', SetRegistrationView.as_view(), name=SetRegistrationView.name),
    url(r'^user/accept_decline/', AcceptDeclinePartnershipView.as_view(), name=AcceptDeclinePartnershipView.name),
    url(r'test/', TestIlDbView.as_view()),
]