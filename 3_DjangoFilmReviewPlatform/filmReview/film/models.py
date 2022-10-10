from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Film(models.Model):
    titel =         models.CharField(max_length=100)
    beschrijving =  models.CharField(max_length=250)
    afbeelding =    models.ImageField(upload_to='film/afbeeldingen/')
    url =           models.URLField(blank=True)