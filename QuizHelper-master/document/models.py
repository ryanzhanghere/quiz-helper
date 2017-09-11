from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    author = models.ForeignKey(User)