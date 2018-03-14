from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
import jwt
import os


class TokenBackend(BaseAuthentication):
    """
    Authentication Backend used for authenticat the Requests.
    We utilize the HTTP-Headers to deliver a JWT token.
    Further we are only interessted if the token valid which
    tells us that the request really comes from the registration;
    not from a exploit skript.
    """

    jwt_secret = None
    jwt_alogrithm = None

    def get_secret_key(self):
        return self.jwt_secret

    def get_algorithm(self):
        return self.jwt_alogrithm

    def get_dummy_user(self):
        return User.objects.get_or_create(username="root")

    def validate_content(self, request, payload):
        """
        We need a generic way to valid the content of the token against
        the provided request data.
        :param request: the request Object
        :param payload: the decoded payload
        :return: boolean
        """
        return True #default

    def authenticate(self, request):
        """
        We define a JWT Authentication only based on the token
        and to related to a database.
        In addition we have the option to compar the encoded data
        with provided data of the request.
        :param request: request
        :return: user object or None
        """
        secret = self.get_secret_key()
        algorithm = self.get_algorithm()

        try:
            token = request.META.get("HTTP_TOKEN")

        except KeyError:
            token = "test"

        payload = ""
        try:
            payload = jwt.decode(token, secret, algorithms=[algorithm])

        except jwt.DecodeError:
            return None
        # option to compare decoded payload with provided data within the request object
        if not self.validate_content(request, payload):
            return None

        user = self.get_dummy_user()

        return user

class UserBackend(TokenBackend):
    """
    The User Validation Backend which uses the secret Key for a User.
    """

    jwt_secret = os.environ.get("JWT_USER_SECRET")
    jwt_alogrithm = os.environ.get("JWT_ALGORITHM")

    def validate_content(self, request, payload):
        """
        We need a generic way to valid the content of the token against
        the provided request data.
        Here we want that the user's lastname and matrikel encoded
        in the token are the same as provided in the request.
        :param request: the request Object
        :param payload: the decoded payload
        :return: boolean
        """
        if request.method == "POST":
            if not (request.data["user_lastname"] == payload["user_lastname"]
                    and request.data["user_matrikel"] == payload["user_matrikel"]):
                return False
        return True


class AdminBackend(TokenBackend):
    """
    The Admin Validation Backend which uses the secret Key for a User.
    """

    jwt_secret = os.environ.get("JWT_ADMIN_SECRET")
    jwt_alogrithm = os.environ.get("JWT_ALGORITHM")

    def get_dummy_user(self):
        return User.objects.get_or_create(username="dummy_admin", is_staff=True)
