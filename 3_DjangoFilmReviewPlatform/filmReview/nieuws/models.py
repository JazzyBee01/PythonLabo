from email.quoprimime import body_check
from django.db import models

# Create your models here.
class Nieuws(models.Model):
    koptekst    = models.CharField(max_length=200)
    body        = models.TextField()
    datum       = models.DateField()

    def __str__(self):
        return self.koptekst