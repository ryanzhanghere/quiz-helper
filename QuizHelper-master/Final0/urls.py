"""Final0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import quiz
import quiz_user
import userprofile

urlpatterns = [
    url(r'^$', 'userprofile.views.user_profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^accounts/', include('userprofile.urls')),

    url(r'^accounts/login/$', 'quiz_user.views.login'),
    url(r'^accounts/auth/$', 'quiz_user.views.auth_view'),
    url(r'^accounts/logout/$', 'quiz_user.views.logout'),
    url(r'^accounts/loggedin/$', 'quiz_user.views.loggedin'),
    url(r'^accounts/invalid/$', 'quiz_user.views.invalid_login'),
    url(r'^accounts/register/$', 'quiz_user.views.register_user'),
    url(r'^accounts/register_success/$', 'quiz_user.views.register_success'),

]
