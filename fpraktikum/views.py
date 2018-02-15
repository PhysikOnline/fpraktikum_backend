# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from import_export.views import ExportViewMixin


# Create your views here.

class ExportView(generics.GenericAPIView, ExportViewMixin):
    queryset = None
    serializer_class = None
    permission_classes = ()
    resource_class = None
    file_name = ""

    def get(self, request, *args, **kwargs):
        resource = self.resource_class()
        data = resource.export()
        headers = resource.get_export_headers()
        response = HttpResponse(content_type="text/csv")
        date = datetime.datetime.now().strftime("%d_%m_%Y")
        response['Content-Disposition'] = 'attachment; filename={0}{1}.csv'.format(self.file_name, date)
        writer = csv.writer(response, dialect=csv.excel)
        writer.writerow(headers)
        for registrant in data:
            writer.writerow(registrant)
        return response