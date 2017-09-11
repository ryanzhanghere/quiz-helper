from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from forms import UserProfileForm
from quiz.models import Quiz

# Create your views here.
@login_required
def user_profile(request):
    """
    user profile page
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)  # populate the form with the original profile
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/loggedin')

    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['username'] = request.user.username
    args['quizzes'] = Quiz.objects.filter(creator=request.user.id)
    return render_to_response('userprofile/profile.html', args)


@login_required
def add_quiz(request):
    """
    Handling add quizzes.
    :param request:
    :return:
    """
    if request.method == 'POST':
        title = request.POST.get("title")
        description = request.POST.get("description")
        print request.user.username
        user = User.objects.get(id=request.user.id)
        print user.email
        Quiz.objects.create(title=title, description=description, creator=user)
    return HttpResponseRedirect('/accounts/profile/')