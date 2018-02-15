from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
import pip

JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"


try:
    import jwt

except ImportError:
    pip.main(["install", "PyJWT"])
    import jwt


class TestBackend(BaseAuthentication):
    """
    Test Authentication Backend used for designing a custom JWT-Authenticationbackend.
    """

    def authenticate(self, request):

        try:
            token = request.data["token"]

        except KeyError:
            token = "test"

        payload = ""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        except jwt.DecodeError:
            return None

        user = User.objects.get_or_create(username="root")

        return user

    def get_user(self, user_id=1):
        return 1