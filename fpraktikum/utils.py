from datetime import datetime
from django.db import connection

"""
This File is for Custom helper functions
"""


def get_semester():

    """
    A helper function to create the Semester acording to the current time of the registration.
    If the registration is createde befor May (5.month) the semester will be a SummerSemester (SS).
    Else it will be a WinterSemester (WS).
    :return: Semeseter<last two digits of year> - string
    """
    current_month = datetime.now().month
    current_year = datetime.now().year
    semester = ''

    if current_month < 5 :
        semester = 'SS{}'.format(str(current_year)[2:4])
    else:
        semester = 'WS{}'.format(str(current_year)[2:4])

    return semester

def il_db_retrieve(user_firstname,user_lastname, user_login, user_mail):
    """
    A Helper function to acces the ILIAS-DB and check wether a user has signed up at
    the Physik-Online eLEarning platform.
    :return: bolean True/False
    """
    with connection['ilias_db'].cursor() as cursor:
        result = cursor.execute(
                        "SELECT usr_id FROM `usr_data` WHERE firstname=%s AND lastname=%s AND login=%s AND email=%s",
                        [user_firstname, user_lastname, user_login, user_mail])
        if result[0]:
            return True
        else:
            return False

