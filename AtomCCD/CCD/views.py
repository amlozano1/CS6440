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
from bs4 import BeautifulSoup


codes = {
    "48765-2": "allergies_reactions_alerts",
    "46240-8": "encounter_history",
    "10157-6": "family_history",
    "11369-6": "immunization_history",
    "10160-0": "medication_history",
    "11450-4": "problem_list",
    "47519-4": "procedures",
    "30954-2": "results",
    "29762-2": "social_history",
    "42348-3": "advanced_directives",
    "48768-6": "payment_sources",
    "8716-3": "physical_findings",
    "42349-1": "reason_for_referral",
    "18776-5": "treatment_plan",
    "47420-5": "functional_status",
    "29549-3": "medication_administered",
    "69730-0": "instructions",

}

# Create your views here.

def index(request):
    return render(request, 'CCD/index.html', {})

@login_required()
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
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            json_chart = parse_ccda(form.cleaned_data['patient'].chart.file.name)
            request.session['CurrentPatient'] = json_chart
            request.session['CurrentPatientXml'] = get_stylish_tables(open(form.cleaned_data['patient'].chart.file.name).read())
            xml_root = remove_namespaces(request.session['CurrentPatientXml'])
            request.session['CurrentPatientTables'] = get_tables(xml_root)
            suffix_tag = xml_root.find("recordTarget").find("patientRole").find("patient").find('name').find("suffix")
            if suffix_tag:
                request.session['middle'] = xml_root.find("recordTarget").find("patientRole").find("patient").find('name').find("suffix").text
            elif 'middle' in request.session:
                del request.session['middle']
            errors = form.errors or None # form not submitted or it has errors
            return render(request, 'CCD/patient_summary.html', {'form': form, 'errors': errors})
    form = PatientForm()
    errors = form.errors or None # form not submitted or it has errors
    return render(request, 'CCD/patient_summary.html', {'form': form, 'errors': errors})


def get_tables(xml_root):
    """
    finds all the tables and their section titles for a CCD
    :param xml_root:
    :return:
    """
    tables = {}
    for section in xml_root.iter("section"):
        if list(section.iter("table")):
            if section.find("code"):
                tables[codes[section.find("code").attrib['code']]] = tostring(section.iter("table").next())
            else:
                tables[section.find("title").text.replace(' ', "_").replace(",", "")] = tostring(section.iter("table").next())
    return tables


def get_stylish_tables(xml):
    soup = BeautifulSoup(xml, "xml")
    tables = soup.find_all('table')
    for table in tables:
        table['class'] = "table table-striped table-bordered table-hover table-responsive"
    theads = soup.find_all('thead')
    for thead in theads:
        thead['data-sortable'] = "true"
    return str(soup)


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