from email.policy import default
from django.db import models

# Create your models here.
class Post (models.Model):
    post_title = models.CharField(max_length=200, default="titel")
    post_text = models.CharField(max_length=2000)
    pub_date = models.DateTimeField('date published')