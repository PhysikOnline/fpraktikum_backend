
class DisableCsrf(object):
    def process_request(self, request):
        return setattr(request, '_dont_enforce_csrf_checks', True)