from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from forms import new_patient_form, PatientForm
from models import Patient
from django.contrib.auth.decorators import login_required
from ccdaparser import parse_ccda
from django.conf import settings
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring

import os
# Create your views here.

def index(request):
    return render(request, 'CCD/index.html', {})

def new_patient(request):
    if request.method == 'POST':
        form = new_patient_form(request.POST, request.FILES)
        if form.is_valid():
            form.add_patient(request.FILES['ccd_file'], form.cleaned_data['Email'])
        else:
            raise Exception("shit!")
        return HttpResponseRedirect('added/')

    else:
        form = new_patient_form()

    return render(request, 'CCD/new_patient.html', {'form': form})

def added(request):
    return render(request, 'CCD/added.html', {})

def login(request):
    pass

@login_required
def dashboard(request):
    print settings.TEMPLATE_CONTEXT_PROCESSORS
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            json_chart = parse_ccda(form.cleaned_data['patient'].chart.file.name)
            request.session['CurrentPatient'] = json_chart
            request.session['CurrentPatientXml'] = open(form.cleaned_data['patient'].chart.file.name).read()
            xml_root = remove_namespaces(request.session['CurrentPatientXml'])

            request.session['CurrentPatientTables'] = get_tables(xml_root)
            errors = form.errors or None # form not submitted or it has errors
            return render(request, 'CCD/dashboard.html', {'form': form, 'errors': errors, })
    form = PatientForm()
    errors = form.errors or None # form not submitted or it has errors
    return render(request, 'CCD/dashboard.html',{'form': form, 'errors': errors, })

@login_required()
def bbhr(request):
    return render(request, 'CCD/BBHR.html')

@login_required()
def view_CCD(request):
    return render(request, 'CCD/patient_summary.html')


def get_tables(xml_root):
    return [tostring(table) for table in xml_root.iter('table')]

def remove_namespaces(xml):
    """
    Returns a xml root, but strips out any namespaces from the tags.
    :type xml: xml to strip namespace from
    """
    from StringIO import StringIO
    it = ET.iterparse(StringIO(xml))
    for _, el in it:
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
    return it.root