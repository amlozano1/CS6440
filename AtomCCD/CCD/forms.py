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
    Email = forms.EmailField()

    def add_patient(self, ccd_file, pref_email):
        #Because of a chicken-egg problem, we need to write the CCDA to disk then have bluebutton parse it before we can
        #pass it to a model
        with NamedTemporaryFile(delete=False) as xml_file:
            for chunk in ccd_file.chunks():
                xml_file.write(chunk)
        ccda = parse_ccda(xml_file.name)
        new_user = User.objects.create_user(pref_email, pref_email, 'password')
        new_user.first_name = ccda['demographics']['name']['given'][0]
        new_user.last_name = ccda['demographics']['name']['family']
        new_user.save()
        new_patient = Patient(user=new_user, chart=ccd_file)
        new_patient.save()

class PatientForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all().order_by('user'), to_field_name="user", empty_label=None)