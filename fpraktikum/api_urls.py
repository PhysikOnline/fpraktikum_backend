from django.conf.urls import url

from fpraktikum.api_views import *

app_name = "api"
urlpatterns = [
    url(r'^registration/', RegistrationView.as_view(), name=RegistrationView.name),
    url(r'^user/(?P<user_login>.+)/', UserCheckView.as_view(), name=UserCheckView.name),
    url(r'^register/', SetRegistrationView.as_view(), name=SetRegistrationView.name),
    url(r'^check_partner/', CheckPartnerView.as_view(), name=CheckPartnerView.name),
    url(r'^accept/', AcceptDeclinePartnershipView.as_view(), name=AcceptDeclinePartnershipView.name),
    url(r'^waitlist/', WaitlistView.as_view(), name=WaitlistView.name),
    url(r'test/', TestIlDbView.as_view()),
]
