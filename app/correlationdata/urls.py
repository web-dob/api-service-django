#-*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'', views.main, name='main'),
    re_path(r'^calculate', views.CalculateView.as_view()),
    re_path(r'^correlation', views.CorrelationView.as_view()),
]