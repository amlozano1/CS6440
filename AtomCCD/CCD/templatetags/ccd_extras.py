__author__ = 'Anthony'
from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime, timedelta, date
from CCD.forms import PatientForm
import bootstrap3
register = template.Library()

@register.filter
@stringfilter
def dob_to_age(string_date):
    """
    Gets the current age in years from a string like 00/00/0000
    :param string_date: a string like 00/00/0000
    :return: Current age in years
    """
    try:
        date = datetime.strptime(string_date, "%d/%m/%Y")
    except Exception:
        try:
            date = datetime.strptime(string_date, "%m/%d/%Y") # I guess date order can be american OR internatl. Great.
        except Exception:
            return 0 # Worst case just say we don't know. #TODO add dateutils package to handle dates. Who the hell wrote the CCD standard and decided NOT to use ISO datestamps???
    return int((datetime.now() - date).days / 365.25)

@register.filter
@stringfilter
def lang(lang_code):
    """
    It seems the CCDs we have for testing are not using ISO 639-1 or any RFC I can find. Bogus. For now we are just
    going to handle them on a case by case basis.
    :param lang_code:
    :return:
    """
    if lang_code == "eng":
        return "English (US)"
    elif lang_code == "fr-CN":  # CN? really? Thats China, not canada. They don't speak french in china.
        return "French (CA)"
    return "None"

@register.simple_tag
def patient_form():
    return PatientForm()
