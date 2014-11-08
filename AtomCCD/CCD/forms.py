__author__ = 'anthony.lozano'
from django import forms
from tempfile import NamedTemporaryFile
from ccdaparser import parse_ccda
from django.contrib.auth.models import User
from models import Patient
import os
from django.conf import settings
import logging
class new_patient_form(forms.Form):

    ccd_file = forms.FileField()

    def add_patient(self, ccd_file):
        #Because of a chicken-egg problem, we need to write the CCDA to disk then have bluebutton parse it before we can
        #pass it to a model
        with NamedTemporaryFile(delete=False) as xml_file:
            for chunk in ccd_file.chunks():
                xml_file.write(chunk)
        ccda = parse_ccda(xml_file.name)
        new_user = User.objects.create_user(ccda['demographics']['name']['given'][0], "marla@fake.me", 'password')
        new_user.last_name = ccda['demographics']['name']['family']
        new_user.save()
        new_patient = Patient(user=new_user, chart=ccd_file)
        new_patient.save()