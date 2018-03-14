from datetime import datetime

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib.auth.models import User

import fpraktikum.models




# This File is for Custom helper functions

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

    if current_month < 5:
        semester = 'SS{}'.format(str(current_year)[2:4])
    else:
        semester = 'WS{}'.format(str(current_year)[2:4])

    return semester


def send_email(data_serializer, status):
    """

    status_options = {"register": ("register", "delete"),
                      "accept": ("accept", "decline"),
                      "waitlist": ("register", "delete"),
                      }
    for overview.
    :param data_serializer : Serializer instance
    :param registrant_data:
    :param partner_data:
    :param registrant_to:
    :param partner_to:
    :param status: ("KEY" OF STATUS OPTIONS , "VALUE" OF STATUS OPTIONS )
    :return:
    """

    templates = {
        # Mail for Single user Registration
        "reg_reg": ["fpraktikum/email/registration_registrant.html",
                    ],

        # Mail for Singel user Deletion
        "reg_del": ["fpraktikum/email/registration_delete_registrant.html",
                    ],

        # Mails if Partner has deleted and Registrant stays
        "reg_del_partner": ["fpraktikum/email/registration_partner_has_deleted.html",
                            "fpraktikum/email/registration_delete_partner.html"],

        # Mail if Registrant deletes but his Partner stays
        "reg_del_partner_stays": ["fpraktikum/email/registration_delete_registrant.html",
                                  "fpraktikum/email/registration_partner_has_deleted.html",
                                  ],

        # Mail for double Registration
        "reg_reg_2": ["fpraktikum/email/registration_registrant.html",
                      "fpraktikum/email/registration_partner.html"],

        # Mail for double Deletion
        "reg_del_2": ["fpraktikum/email/registration_delete_registrant.html",
                      "fpraktikum/email/registration_delete_partner.html"],

        # Mail for Waitlistregistration
        "waitlist_reg": ["fpraktikum/email/waitlist_register.html",
                         ],

        # Mail for Waitlist deletion
        "waitlist_del": ["fpraktikum/email/waitlist_delete.html",
                         ],

        # Mail if partner accapts Partnership
        "accept_acc": ["fpraktikum/email/accept_registrant.html",
                       "fpraktikum/email/accept_partner.html"],

        # Mail if partner declines Partnership
        "accept_dec": ["fpraktikum/email/accept_registrant_decline.html",
                       "fpraktikum/email/accept_partner_decline.html"],
    }
    subject = "Fortgeschrittenen Praktikum"
    from_email = "elearning@itp.uni-frankfurt.de"

    registrant_data = {
        "user_firstname":data_serializer.user_firstname,
        "user_lastname": data_serializer.user_lastname,
    }

    registrant_to = data_serializer.user_mail

    context_data = ((registrant_data, registrant_to), )

    try:
        partner = data_serializer.partner
    except (fpraktikum.models.FpUserPartner.DoesNotExist, AttributeError):
        partner = None
    else:
        partner_data = {
            "user_firstname": partner.user_firstname,
            "user_lastname": partner.user_lastname,
            "registrant_firstname": data_serializer.user_firstname,
            "registrant_lastname": data_serializer.user_lastname

        }

        partner_to = data_serializer.partner.user_mail

        context_data += ((partner_data, partner_to),)

        if status == "reg_reg" or status == "reg_del":
            status += "_2"

    index = 0

    for tmp in templates[status]:
        context = context_data[index][0]
        to_mail = [context_data[index][1], ]

        message = get_template(tmp).render(context)
        mail = EmailMessage(subject, message, to=to_mail, from_email=from_email)
        mail.content_subtype = 'html'
        mail.send()
        index += 1
