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

    def get_algoithm(self):
        return self.jwt_alogrithm

    def get_dummy_user(self):
        return User.objects.get_or_create(username="root")

    def authenticate(self, request):

        secret = self.get_secret_key()
        algorithm = self.get_algoithm()

        try:
            token = request.META.get("HTTP_TOKEN")

        except KeyError:
            token = "test"

        payload = ""
        try:
            payload = jwt.decode(token, secret, algorithms=[algorithm])

        except jwt.DecodeError:
            return None

        user = self.get_dummy_user()

        return user

class UserBackend(TokenBackend):
    """
    The User Validation Backend which uses the secret Key for a User.
    """

    jwt_secret = os.environ.get("JWT_USER_SECRET")
    jwt_alogrithm = os.environ.get("JWT_ALGORITHM")

class AdminBackend(TokenBackend):
    """
    The Admin Validation Backend which uses the secret Key for a User.
    """

    jwt_secret = os.environ.get("JWT_ADMIN_SECRET")
    jwt_alogrithm = os.environ.get("JWT_ALGORITHM")

    def get_dummy_user(self):
        return User.objects.get_or_create(username="dummy_admin", is_staff=True)