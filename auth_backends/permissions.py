from rest_framework.permissions import BasePermission

class OnlyAdminGet(BasePermission):
    """
    We have a few views where the GET method is only allowed for admin users
    """

    def has_permission(self, request, view):

        if request.method == "GET":

            if request.user.is_staff:   # we allow GET only for admins
                return True
            return False                # if not its disallows

        return request.user and request.user.is_authenticated