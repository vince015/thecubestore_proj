from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q

from django.views.defaults import server_error
from django.core.exceptions import PermissionDenied

from system_app.models import Item, Sales, Payout, Contact, Cube, Payout, Profile
from util.util import SYSTEM_APP_LOGIN, is_crew

INVALID_CREDENTIALS = "Invalid username and/or password"
INACTIVE_USER = "User is inactive."
NOT_CREW = "You are authenticated as {0}, but are not authorized to access this page. Would you like to login to a different account?"

def user_login(request):

    try:
        # Redirection
        template = 'system_app/login.html'
        redirect = request.GET.get('next', '/system/dashboard')

        context_dict = dict()
        context_dict['redirect_to'] = redirect

        if not request.user.is_anonymous() and not is_crew(request.user):
            messages.error(request, NOT_CREW.format(request.user))

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect)
                else:
                    messages.error(request, INACTIVE_USER)
                    return render(request, template)
            else:
                messages.error(request, INVALID_CREDENTIALS)
                return render(request, template, context_dict)

    except Exception as e:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(SYSTEM_APP_LOGIN)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def dashboard(request):

    try:
        context_dict = dict()
        template = 'system_app/dashboard.html'

        user = User.objects.get(username=request.user.username)
        context_dict['user'] = user

        items = Item.objects.all()
        context_dict['items'] = items[:10]

    except Exception as ex:
        return server_error(request)

    return render(request, template, context_dict)

@login_required()
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def search(request):

    try:
        context_dict = dict()
        template = 'system_app/dashboard/search.html'

        q = request.GET.get('q')
        if q:
            items = Item.objects.filter(Q(description__icontains=q) |
                                        Q(code__icontains=q) )
            context_dict['items'] = items
        else:
            items = Item.objects.all()[:10]
            context_dict['items'] = items

    except Exception as e:
        raise e

    return render(request, template, context_dict)

@login_required()
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def buy(request, item_id):

    try:
        context_dict = dict()
        template = 'system_app/dashboard/buy.html'

        item = Item.objects.get(pk=item_id)
        context_dict['item'] = item

    except Exception as e:
        raise e

    return render(request, template, context_dict)
