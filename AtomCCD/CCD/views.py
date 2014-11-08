from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from forms import new_patient_form
# Create your views here.


# class New_Patient_View(FormView):
#     template = 'CCD/new_patient.html'
#     form_class = new_patient_form
#     success_url = '/patient_added/'
#
#     def form_valid(self, form):
#         form.add_patient()
#         return super(New_Patient_View, self).form_valid(form)

def index(request):
    return render(request, 'CCD/index.html', {})

def new_patient(request):
    if request.method == 'POST':
        form = new_patient_form(request.POST, request.FILES)
        if form.is_valid():
            form.add_patient(request.FILES['ccd_file'], form.cleaned_data['pref_email'])
        else:
            raise Exception("shit!")
        return HttpResponseRedirect('added/')

    else:
        form = new_patient_form()

    return render(request, 'CCD/new_patient.html', {'form': form})

def added(request):
    return render(request, 'CCD/added.html', {})