from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.defaults import server_error
from django.core.exceptions import PermissionDenied

from system_app.models import Item, Sales, Payout, Contact, Cube, Payout, Profile

INVALID_CREDENTIALS = "Invalid username and/or password"
INACTIVE_USER = "User is inactive."

import json

def is_member(user, group):
    return user.groups.filter(name=group).exists()

def user_login(request):

    try:
        # Redirection
        template = 'system_app/login.html'

        redirect = request.GET.get('next', '/system/dashboard')
        if not redirect.startswith('/system'):
            raise Http404

        context_dict = dict()
        context_dict['redirect_to'] = redirect

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

    except:
        return server_error(request)

    return render(request, template, context_dict)

def user_logout(request):

    logout(request)
    return HttpResponseRedirect('/system/login/')

@login_required
def dashboard(request):

    try:
        context_dict = dict()
        template = 'system_app/dashboard.html'

        user = User.objects.get(username=request.user.username)
        context_dict['user'] = user

        # Get user info
        if is_member(user, 'Crew'):
            items = Item.objects.all()
            context_dict['items'] = items

            sales = Sales.objects.all().order_by('-date')
            context_dict['sales'] = sales

            unpaid = 0
            for sale in sales:
                if not sale.payout:
                    unpaid = unpaid + sale.net
            context_dict['unpaid'] = unpaid

            payouts = Payout.objects.all().order_by('-date')
            context_dict['payouts'] = payouts

            context_dict['merchants'] = list()
            cubes = Cube.objects.all().order_by('-next_due_date')
            for cube in cubes:
                merchant = cube.user.__dict__
                profile = Profile.objects.filter(user=cube.user).first()
                if profile:
                    merchant.update(profile.__dict__)
                contact = Contact.objects.filter(user=cube.user).first()

                merchant_info = {'profile': merchant,
                                 'contact': contact,
                                 'cube': cube}

                context_dict['merchants'].append(merchant_info)

        else:
            raise PermissionDenied

    except PermissionDenied:
        logout(request)
        raise

    except Exception as ex:
        raise
        return server_error(request)

    return render(request, template, context_dict)
