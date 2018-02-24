from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from rest_framework import permissions
from django.urls import reverse


schema_view = get_schema_view(
    openapi.Info(
        title="PO-FP API",
        default_version='v1.0',
        description="This is the API for the FP integration",
        contact=openapi.Contact(email="christian@elearning.physik.uni-frankfurt.de"),
    ),
   # validators=['ssv', 'flex'],
    public=True,
    permission_classes=(permissions.IsAdminUser,),
    url="https://po-fp-staging.physikelearning.de/api/", # hard coded for now
)

urlpatterns = [
    url(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    ]