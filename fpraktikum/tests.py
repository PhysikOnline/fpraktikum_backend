# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import SimpleTestCase

from fpraktikum.utils import il_db_retrieve
# Create your tests here.


# This test doesn't work yet because django tries to build a test_database out of the specified 'ilias_db' which should not happen.
# we test this function via a dummy api View in api_views.py


# class ILDbTestCase(SimpleTestCase):
#
#     self.user_firstname = 'Christian Rudolph Friedrich'
#     self.user_lastname = 'Grossmüller'
#     self.user_login = 's5935755'
#     self.user_mail = 's5935755@rz.uni-frankfurt.de'
#
#     def test_with_vaild_data(self):
#         result = il_db_retrieve(user_firstname=self.user_name,
#                                 user_lastname=self.user_lastname,
#                                 user_login=self.user_login,
#                                 user_mail=self.user_mail
#                                 )
#         assert result #should be True for this data
