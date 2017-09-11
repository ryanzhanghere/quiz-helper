from django.db import models
from quiz.models import Quiz
from django.contrib.auth.models import User


# Nested comments implementation referenced to http://www.maxburstein.com/blog/django-threaded-comments/
# Create your models here.
class Comment(models.Model):
    quiz_id = models.ForeignKey(Quiz, verbose_name="related quiz")
    quote_id = models.ForeignKey('self', null=True, blank=True, verbose_name="Quoted comment")
    comment_body = models.CharField(max_length=800, blank=False)
    creator = models.ForeignKey(User, null=False, blank=False)
    path = models.CommaSeparatedIntegerField(max_length=255, null=True)
    depth = models.PositiveSmallIntegerField(default=0)

    date = models.DateTimeField(auto_now_add=True, verbose_name="date and time created")

    def __str__(self):
        """
        String representation for Project in database.
        :return: String representation for Project in database.
        """
        return self.comment_body[0:50]
