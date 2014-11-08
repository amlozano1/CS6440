from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Atom(models.Model):
    logic = models.CharField(max_length=100)  # Just a dummy until we figure this out for real
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.ForeignKey(User)
    chart = models.FileField()

class Physician(models.Model):
    patients = models.ManyToManyField(Patient)