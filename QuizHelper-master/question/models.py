from django.db import models
from quiz.models import Quiz


# Create your models here.
class EssayQuestion(models.Model):
    question_body = models.TextField(verbose_name='Question', blank=False, help_text='Description of the question.')
    answer = models.TextField(verbose_name='Answer', blank=False, help_text='Answer')
    quiz = models.ForeignKey(Quiz, null=False, blank=False)

    def __str__(self):
        """
        String representation of the object in database.
        :return: question_body, a string
        """
        return self.question_body


class MultipleChoiceQuestion(models.Model):
    question_body = models.TextField(verbose_name='Question', blank=False, help_text='Description of the question.')
    correct_answer = models.TextField(verbose_name='Correct answer', blank=False, help_text='Description of the answer.')
    quiz = models.ForeignKey(Quiz, null=True, blank=True)

    def __str__(self):
        """
        String representation of the object in database.
        :return: question_body, a string
        """
        return self.question_body


class MultipleChoiceAnswer(models.Model):
    answer_body = models.TextField(verbose_name='Answer', blank=False, help_text='Description of the answer')
    question = models.ForeignKey(MultipleChoiceQuestion, null=True, blank=False)  # the corresponding question

    def __str__(self):
        """
        String representation of the object in database.
        :return: answer_body, a string
        """
        return self.answer_body
