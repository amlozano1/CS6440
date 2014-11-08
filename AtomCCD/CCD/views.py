from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from forms import new_patient_form, PatientForm
from models import Patient
from django.contrib.auth.decorators import login_required

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
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid:
            pass # TODO Redirect to CCD viewr
    form = PatientForm()
    errors = form.errors or None # form not submitted or it has errors
    return render(request, 'CCD/dashboard.html',{'form': form, 'errors': errors, })