# -*- coding: utf-8 -*-

from rest_framework.exceptions import ValidationError

from fpraktikum.ilias_model import UsrData
from fpraktikum.models import FpUserRegistrant, FpUserPartner, FpWaitlist
#from fpraktikum.models import FpUserRegistrant, FpUserPartner, FpWaitlist, FpInstitute
#from fpraktikum.serializers import (FpFullUserPartnerSerializer, FpFullUserRegistrantSerializer, FpWaitlistSerializer)


def il_db_retrieve(user_lastname, user_login, user_matrikel=None, user_firstname=None, user_mail=None):
    """

    A Helper function to acces the ILIAS-DB and check wether a user has signed up at
    the Physik-Online eLEarning platform.
    It is used once for evaluatiing a User then there are all Parameter given.
    The second use is to check if a Partner is registerd at the platform; then only login and lastname are given.

    :return: bolean True/False
    """

    try:
        user = UsrData.objects.using('ilias_db').get(lastname=user_lastname, login=user_login)
    except UsrData.DoesNotExist:
        return None
    else:
        data = {"user_firstname": user.firstname,
                "user_lastname": user.lastname,
                "user_login": user.login,
                "user_mail": user.email,
                "user_matrikel": user.matriculation
                }
        return data


def is_user_valid(login):

    models = (FpUserRegistrant, FpUserPartner, FpWaitlist)

    for m in models:
        try:
            m.objects.get(user_login=login)
        except m.DoesNotExist:
            pass
        else:
            return False

    return True

# no longer needed

# def check_user(login):
#     """
#     This function will provide the current registration status of the student.
#
#     :param login: <str>
#     :param semester:  <str>
#     :return: Data of the student in the context of the Fpraktikum Registration
#     """
#
#     import fpraktikum.serializers
#
#     models = {"registrant": (FpUserRegistrant, fpraktikum.serializers.FpFullUserRegistrantSerializer),
#               "partner": (FpUserPartner, fpraktikum.serializers.FpFullUserPartnerSerializer),
#               "waitlist": (FpWaitlist, fpraktikum.serializers.FpWaitlistSerializer),
#               }
#     return_value = {"data": {},
#                     "status": None,
#                     }
#     for k, v in models.items():
#         try:
#             user = v[0].objects.get(user_login=login)
#
#         except v[0].DoesNotExist:
#             pass
#
#         else:
#             return_value = {"data": v[1](user).data,
#                             "status": k,
#                             }
#
#     return return_value


def check_institute(institute_one, institute_two=None):
    """
    This Function helps to evaluate if the given institutes are in the system.
    And : both institutes may not have the same semesterhalf,
          both institutes may not have the same name,
          both institutes need to have the same graduation.
    :param institute_one: <dict>
    :param institute_two: None or <dict>
    :return:
    """
    if institute_two:
        if institute_two["semesterhalf"] == institute_one["semesterhalf"]:
            raise ValidationError(detail=u"Die Semesterhälften müssen unterschiedlich sein.")
        if institute_two["semesterhalf"] == 3 or institute_one["semesterhalf"] == 3:
            raise ValidationError(
                detail=u"Eines der Institute wird für beide Semesterhälften belegt, bitte wähle nur dieses aus.")
        if institute_two["name"] == institute_one["name"]:
            raise ValidationError(detail=u"Es müssen 2 unterschiedliche Institute ausgewählt werden.")
        if not institute_two["graduation"] == institute_one["graduation"]:
            raise ValidationError(detail=u"Es müssen Institute mit dem gleichen Abschluss gewählt werden.")
        # now try to recieve the institute
        inst_one = FpInstitute.objects.get(name=institute_one["name"],
                                           graduation=institute_one["graduation"],
                                           semesterhalf=institute_one["semesterhalf"])
        inst_two = FpInstitute.objects.get(name=institute_two["name"],
                                           graduation=institute_two["graduation"],
                                           semesterhalf=institute_two["semesterhalf"])

        return (inst_one, inst_two)

    else:
        inst_one = inst_one = FpInstitute.objects.get(name=institute_one["name"],
                                                      graduation=institute_one["graduation"],
                                                      semesterhalf=institute_one["semesterhalf"])

        return (inst_one,)


def inst_recover(institute_one, places, institute_two=None):
    if institute_two:
        institute_one.places += places
        institute_two.places += places
        institute_one.save()
        institute_two.save()
    else:
        institute_one.places += places
        institute_one.save()
