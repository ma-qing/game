# -*- coding: utf-8 -*-
from django.conf.urls import url

from Interaction import views

urlpatterns = [
    url("^showconfig$", views.showconfig)
]