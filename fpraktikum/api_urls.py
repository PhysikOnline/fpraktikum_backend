from django.conf.urls import url

from rest_framework.routers import SimpleRouter

from fpraktikum.api_views import *


app_name = "api"
urlpatterns = [
    url(r'^user/(?P<user_login>.+)/', UserCheckView.as_view(), name=UserCheckView.name),
    url(r'^check_partner/', CheckPartnerView.as_view(), name=CheckPartnerView.name),
    url(r'^export_reg', ExportRegistrantsView.as_view()),
    url(r'^export_wait', ExportWaitlistView.as_view()),
    url(r'registration/current', CurrentRegistrationView.as_view())
]

router = SimpleRouter()
router.register(r'user_registrant', UserRegistrantViewset)
router.register(r'user_partner', UserPartnerViewset)
router.register(r'waitlist', WaitlistView)
router.register(r'registration', RegistrationView)

urlpatterns += router.urls
