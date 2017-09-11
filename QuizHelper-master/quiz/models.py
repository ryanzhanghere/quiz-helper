from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Quiz(models.Model):
    title = models.CharField(verbose_name='Title', max_length=70, blank=False)
    description = models.TextField(verbose_name='Description', blank=True, help_text='Description of the quiz.')
    creator = models.ForeignKey(User, null=False, blank=False)

    def __str__(self):
        """
        String representation of the object in database.
        :return: title, a string
        """
        return self.title
