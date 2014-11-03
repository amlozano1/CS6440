__author__ = 'anthony.lozano'
from django.conf.urls import patterns, url

from CCD import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)