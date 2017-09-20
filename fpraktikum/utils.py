from datetime import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

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

    if current_month < 5:
        semester = 'SS{}'.format(str(current_year)[2:4])
    else:
        semester = 'WS{}'.format(str(current_year)[2:4])

    return semester


def send_email(registrant_data={}, partner_data={}, registrant_to=None, partner_to=None, status=None):
    """

    status_options = {"register": ("register", "delete"),
                      "accept": ("accept", "decline"),
                      "waitlist": ("register", "delete"),
                      }
    for overview.

    :param registrant_data:
    :param partner_data:
    :param registrant_to:
    :param partner_to:
    :param status: ("KEY" OF STATUS OPTIONS , "VALUE" OF STATUS OPTIONS )
    :return:
    """
    data = ((registrant_data, registrant_to), (partner_data, partner_to))
    templates = {"reg_reg_1": ["fpraktikum/email/registration_registrant.html",
                               ],

                 "reg_del_1": ["fpraktikum/email/registration_delete_registrant.html",
                               ],
                 "reg_del_partner": ["fpraktikum/email/registration_delete_partner.html",
                                     "fpraktikum/email/registration_parnter_has_deleted.html"],
                 "reg_del_partner_stays": ["fpraktikum/email/registration_delete_registrant.html",
                                           "fpraktikum/email/registration_parnter_has_deleted.html",
                                           ],

                 "reg_reg_2": ["fpraktikum/email/registration_registrant.html",
                               "fpraktikum/email/registration_partner.html"],

                 "reg_del_2": ["fpraktikum/email/registration_delete_registrant.html",
                               "fpraktikum/email/registration_delete_partner.html"],

                 "waitlist_reg": ["fpraktikum/email/waitlist_register.html",
                                  ],

                 "waitlist_del": ["fpraktikum/email/waitlist_delete.html",
                                  ],

                 "accept_acc": ["fpraktikum/email/accept_registrant.html",
                                "fpraktikum/email/accept_partner.html"],

                 "accept_dec": ["fpraktikum/email/accept_registrant_decline.html",
                                "fpraktikum/email/accept_partner_decline.html"],
                 }
    subject = "Fortgeschrittenen Praktikum"
    from_email = "elearning@physik.uni-frankfurt.de"
    index = 0
    for tmp in templates["status"]:
        context = data[index][0]
        to_mail = data[index][1]

        message = get_template(tmp).render(Context(context))
        mail = EmailMessage(subject, message, to=to_mail, from_email=from_email)
        mail.content_subtype = 'html'
        mail.send()
        index += 1


