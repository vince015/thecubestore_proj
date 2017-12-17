from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error
from django.core.exceptions import PermissionDenied

from system_app.models import Contact, Store, Bank, Announcement, Profile
from system_app.models import Cube, Payout, Item, Sales
from util.util import VIEWER_APP_LOGIN, is_merchant


INVALID_CREDENTIALS = "Invalid username and/or password"
INACTIVE_USER = "User is inactive."
NOT_MERCHANT = "You are authenticated as {0}, but are not authorized to access this page. Would you like to login to a different account?"

def is_member(user, group):
    return user.groups.filter(name=group).exists()

def user_login(request):

    try:
        # Redirection
        template = 'viewer_app/login.html'
        redirect = request.GET.get('next', '/thecubestore')

        context_dict = dict()
        context_dict['redirect_to'] = redirect

        if not request.user.is_anonymous() and not is_member(request.user, 'Merchant'):
            messages.error(request, NOT_MERCHANT.format(request.user))

        announcement = Announcement.objects.all().order_by('-issue_date')
        if announcement:
            context_dict['announcement'] = announcement[0]

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

@login_required
@user_passes_test(is_merchant, login_url=VIEWER_APP_LOGIN)
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(VIEWER_APP_LOGIN)

@login_required
@user_passes_test(is_merchant, login_url=VIEWER_APP_LOGIN)
def change_password(request):

    try:
        template = 'viewer_app/password.html'
        context_dict = dict()

        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            context_dict['form'] = form

            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')

                return redirect('/thecubestore/profile')
        else:
            form = PasswordChangeForm(request.user)
            context_dict['form'] = form

    except:
        return server_error(request)

    return render(request, template, context_dict)


@login_required
@user_passes_test(is_merchant, login_url=VIEWER_APP_LOGIN)
def profile(request):

    try:
        context_dict = dict()
        template = 'viewer_app/profile.html'

        user = User.objects.get(username=request.user.username)
        context_dict['profile'] = user.__dict__

        profile = Profile.objects.filter(user=user).first()
        if profile:
            context_dict['profile'].update(profile.__dict__)

            sales = Sales.objects.filter(item__startswith=profile.merchant_id).order_by('-date')
            context_dict['sales'] = sales

            # Get Sales
            unpaid = 0
            for sale in sales:
                if not sale.payout:
                    unpaid = unpaid + sale.net
            context_dict['unpaid'] = unpaid

        contact = Contact.objects.filter(user=user).first()
        if contact:
            context_dict['contact'] = contact

        store = Store.objects.filter(user=user).first()
        if store:
            context_dict['store'] = store

        bank = Bank.objects.filter(user=user).first()
        if bank:
            context_dict['bank']  = bank

        cubes = Cube.objects.filter(user=user).order_by('-next_due_date')
        context_dict['cubes'] = cubes

        # Get inventory from cube
        context_dict['items'] = list()
        for cube in cubes:
            items = Item.objects.filter(cube=cube)
            for item in items:
                context_dict['items'].append(item)

        payouts = Payout.objects.filter(merchant=user).order_by('-date')
        context_dict['payouts'] = payouts

        earnings = 0
        for payout in payouts:
            earnings = earnings + payout.amount
        context_dict['earnings'] = earnings

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_merchant, login_url=VIEWER_APP_LOGIN)
def cube(request, cube_id):

    try:
        template = 'viewer_app/cube.html'
        context_dict = dict()

        cube = Cube.objects.get(id=cube_id,
                                user=request.user)
        context_dict['cube'] = cube

        items = Item.objects.filter(cube=cube)
        context_dict['items'] = items

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_merchant, login_url=VIEWER_APP_LOGIN)
def item(request, item_id):

    try:
        template = 'viewer_app/item.html'
        context_dict = dict()

        item = Item.objects.get(id=item_id,
                                cube__user=request.user)
        context_dict['item'] = item

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_merchant, login_url=VIEWER_APP_LOGIN)
def payout(request, payout_id):

    try:
        template = 'viewer_app/payout.html'
        context_dict = dict()

        payout = Payout.objects.get(id=payout_id)
        context_dict['payout'] = payout

        sales = Sales.objects.filter(payout=payout.id).order_by('-date')
        context_dict['sales'] = sales

        sale_sum = 0
        for sale in sales:
            sale_sum = sale_sum + sale.net
        context_dict['sum'] = sale_sum

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

