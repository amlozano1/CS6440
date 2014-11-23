__author__ = 'anthony.lozano'
from django.conf.urls import patterns, url

from CCD import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new_patient/added/', views.added, name='added'),
    url(r'^new_patient/', views.new_patient, name='new_patient'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^bbhr/', views.bbhr, name='bbhr'),
)