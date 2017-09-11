from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from forms import RegistrationForm

# Create your views here.
def login(request):
    """
    Login page
    :param request:
    :return:
    """
    context = {}
    context.update(csrf(request))
    return render_to_response('quiz_user/login.html', context)


def auth_view(request):
    """
    authentication
    :param request:
    :return:
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/profile')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
    """
    Indicating loggedin
    :param request:
    :return:
    """
    return render_to_response('quiz_user/loggedin.html', {'full_name': request.user.username})


def invalid_login(request):
    """
    Login failure page
    :param request:
    :return:
    """
    return render_to_response('quiz_user/invalid_login.html')


def logout(request):
    """
    Logout request handling
    :param request:
    :return:
    """
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')
    # return render_to_response('quiz_user/logout.html')


def register_user(request):
    """
    Handle registration
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/login')

    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()  # Initialize a form
    return render_to_response('quiz_user/register.html', args)


def register_success(request):
    """
    Successful registration handling
    :param request:
    :return:
    """
    return render_to_response('quiz_user/register_success.html')