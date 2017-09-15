from fpraktikum.ilias_model import UsrData
from fpraktikum.models import FpUserRegistrant, FpUserPartner, FpWaitlist
from fpraktikum.serializers import (FpFullUserPartnerSerializer, FpFullUserRegistrantSerializer, FpWaitlistSerializer,
                                    RegistrationSerializer)


def il_db_retrieve(user_lastname, user_login, user_matrikel=None, user_firstname=None, user_mail=None):
    """

    A Helper function to acces the ILIAS-DB and check wether a user has signed up at
    the Physik-Online eLEarning platform.
    It is used once for evaluatiing a User then there are all Parameter given.
    The second use is to check if a Partner is registerd at the platform; then only login and lastname are given.

    :return: bolean True/False
    """

    if user_firstname and user_mail and user_matrikel:
        try:
            user = UsrData.objects.get(firstname=user_firstname, lastname=user_lastname,
                                       login=user_login, email=user_mail)
        except UsrData.DoesNotExist:
            return None
        else:
            data = {"user_firstname":user_firstname,
                    "user_lastname": user_lastname,
                    "user_login": user_login,
                    "user_mail": user_mail,
                    "user_matrikel": user_matrikel
                    }
            return data
    else:
        try:
            user = UsrData.objects.get(user_lastname=user_lastname, user_login=user_login)
        except UsrData.DoesNotExist:
            return None
        else:
            data = {"user_firstname": user.user_firstname,
                    "user_lastname": user.user_lastname,
                    "user_login": user.user_login,
                    "user_mail": user.user_mail,
                    "user_matrikel": user.user_matrikel
                    }
            return data

    # try:
    #     query = UsrData.objects.using('ilias_db').get(firstname=user_firstname, lastname=user_lastname,
    #                                                   login=user_login, email=user_mail)
    #
    # except UsrData.DoesNotExist:
    #     return False
    #
    # return query.usr_id


def check_user(login):
    """
    This function will provide the current registration status of the student.

    :param login: <str>
    :param semester:  <str>
    :return: Data of the student in the context of the Fpraktikum Registration
    """

    models = {"registrant": (FpUserRegistrant, FpFullUserRegistrantSerializer),
              "partner": (FpUserPartner, FpFullUserPartnerSerializer),
              "waitlist": (FpWaitlist, FpWaitlistSerializer),
              }
    return_value = {"data": {},
                    "status": None,
                    }
    for k, v in models.iteritems():
        try:
            user = v[0].objects.get(user_login=login)

        except v[0].DoesNotExist:
            pass

        else:
            return_value = {"data": v[1](user).data,
                            "status": k,
                            }

    return return_value


def validate_registration_data(data):

    serializer = RegistrationSerializer()

    try:
        serializer.run_validation(data=data)
    except serializer.ValidationError:
        return False
    else:
        return True
