# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView

# Create your views here.


class MyView(LoginRequiredMixin, TemplateView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "test.html"



