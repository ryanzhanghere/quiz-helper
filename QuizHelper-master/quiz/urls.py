from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='quiz-index'),
    url(r'^add_question$', views.add_question, name='add-question'),
    url(r'^add_multiple_choice_question', views.add_multiple_choice_question, name='add multi choice question'),
    url(r'^add_comment$', views.add_comment, name='add comment'),
    url(r'^all_quizzes$', views.all_quizzes, name='all quizzes'),
    url(r'^upload$', views.create_quiz_from_file, name='add quiz from file'),
]
