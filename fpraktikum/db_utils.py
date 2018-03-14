# -*- coding: utf-8 -*-

from fpraktikum.ilias_model import UsrData
from fpraktikum.models import FpUserRegistrant, FpUserPartner, FpWaitlist
import datetime
import csv
from django.http import HttpResponse
from rest_framework import generics

def il_db_retrieve(user_lastname, user_login):
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
