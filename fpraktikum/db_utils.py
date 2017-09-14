from fpraktikum.ilias_model import UsrData
from fpraktikum.models import FpUserRegistrant, FpUserPartner, FpWaitlist
from fpraktikum.serializers import FpFullUserPartnerSerializer, FpFullUserRegistrantSerializer, FpWaitlistSerializer


def il_db_retrieve(user_firstname, user_lastname, user_login, user_mail):
    """
    A Helper function to acces the ILIAS-DB and check wether a user has signed up at
    the Physik-Online eLEarning platform.
    :return: bolean True/False
    """
    try:
        query = UsrData.objects.using('ilias_db').get(firstname=user_firstname, lastname=user_lastname,
                                                      login=user_login, email=user_mail)

    except UsrData.DoesNotExist:
        return False

    return query.usr_id


def check_user(login):
    """
    This function will provide the current registration status of the student.

    :param user_login: <str>
    :param semester:  <str>
    :return: Data of the student in the context of the Fpraktikum Registration
    """

    models = {"registrant": (FpUserRegistrant, FpFullUserRegistrantSerializer),
              "partner": (FpUserPartner, FpFullUserPartnerSerializer),
              "waitlist": (FpWaitlist, FpWaitlistSerializer),
              }
    not_registerd_user = {"data": "",
                          "status": None,
                          }
    return_value = {}
    for k, v in models.iteritems():
        try:
            user = v[0].objects.get(user_login=login)

        except v[0].DoesNotExist:
            pass

        else:
            return_value = {"data": v[1](user).data,
                            "status": k,
                            }

    return return_value if (return_value["data"] and return_value["status"]) else not_registerd_user