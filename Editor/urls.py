# -*- coding: utf-8 -*-
from django.conf.urls import url

from Editor import views

urlpatterns = [
    url("^login$", views.login),
]