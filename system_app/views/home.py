from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.defaults import server_error
from django.core.exceptions import PermissionDenied


INVALID_CREDENTIALS = "Invalid username and/or password"
INACTIVE_USER = "User is inactive."

def is_member(user, group):
    return user.groups.filter(name=group).exists()

def user_login(request):

    try:
        # Redirection
        template = 'login.html'
        next = request.GET.get('next', '/system')

        context_dict = dict()
        context_dict['redirect_to'] = next
     
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(next)
                else:
                    messages.error(request, INACTIVE_USER)
                    return render(request, template)
            else:
                messages.error(request, INVALID_CREDENTIALS)
                return render(request, template, context_dict)

    except:
        return server_error(request)

    return render(request, template, context_dict)

def user_logout(request):

    logout(request)
    return HttpResponseRedirect('/system')

@login_required
def dashboard(request):

    try:
        context_dict = dict()
        template = 'system_app/dashboard.html'

        user = User.objects.get(username=request.user.username)
        context_dict['user'] = user

        # Get user info
        if is_member(user, 'Staff'):
            pass

        else:
            raise PermissionDenied

    except PermissionDenied:
        logout(request)
        raise
           
    except Exception as ex:
        logout(request)
        return server_error(request)

    return render(request, template, context_dict)