from rest_framework.permissions import BasePermission

class OnlyAdminMethodPermission(BasePermission):
    """
    A generic Permission which allows certain HTTP methods only
    for admins.
    """
    methods = ()

    def get_methods(self):
        return self.methods

    def has_permission(self, request, view):

        methods = self.get_methods()

        if request.method in methods:
            if request.user.is_staff:   # we allow GET only for admins
                return True
            return False                # if not it disallows

        return request.user and request.user.is_authenticated


class OnlyAdminGet(OnlyAdminMethodPermission):
    """
    We have a few views where the GET method is only allowed for admin users
    """
    methods = ("GET",)


class OnlyAdminPostDelete(OnlyAdminMethodPermission):
    """
    We have a view where only Admins are allowed to POST or UPDATE
    """

    methods = ("POST", "PUT", "DELETE")