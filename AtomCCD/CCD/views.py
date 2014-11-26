from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from forms import new_patient_form, PatientForm
from models import Patient
from django.contrib.auth.decorators import login_required
from ccdaparser import parse_ccda
from django.conf import settings
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
            errors = form.errors or None # form not submitted or it has errors
            return render(request, 'CCD/dashboard.html', {'form': form, 'errors': errors, })
    form = PatientForm()
    errors = form.errors or None # form not submitted or it has errors
    #middle = xml_root.find("recordTarget").find("patientRole").find("patient").find("suffix").text
    return render(request, 'CCD/dashboard.html',{'form': form, 'errors': errors, })

@login_required()
def view_CCD(request):
    pass