from django.db import models

# Create your models here.


class Atom(models.Model):
    logic = models.CharField(max_length=100)  # Just a dummy until we figure this out for real
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



