from django.conf.urls import patterns, include, url
from . import views
urlpatterns = [
    url(r'^profile/$', views.user_profile, name='profile'),
    url(r'^profile/add_quiz$', views.add_quiz, name="add-quiz"),
]
