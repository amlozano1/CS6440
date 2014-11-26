__author__ = 'Anthony'
from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime, timedelta, date

register = template.Library()

@register.filter
@stringfilter
def dob_to_age(string_date):
    """
    Gets the current age in years from a string like 00/00/0000
    :param string_date: a string like 00/00/0000
    :return: Current age in years
    """
    date = datetime.strptime(string_date, "%d/%m/%Y")
    return int((datetime.now() - date).days / 365.25)