from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error
from django.core.exceptions import PermissionDenied

from system_app.models import Contact, Store, Bank
from system_app.models import Cube, Payout, Item, Sales


INVALID_CREDENTIALS = "Invalid username and/or password"
INACTIVE_USER = "User is inactive."

def is_member(user, group):
    return user.groups.filter(name=group).exists()

def user_login(request):

    try:
        # Redirection
        template = 'viewer_app/login.html'
        next = request.GET.get('next', '/thecubestore')

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
    return HttpResponseRedirect('/thecubestore/login')

@login_required
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
        raise
        return server_error(request)

    return render(request, template, context_dict)


@login_required
def profile(request):

    try:
        context_dict = dict()
        template = 'viewer_app/profile.html'

        user = User.objects.get(username=request.user.username)
        context_dict['profile'] = user

        # Get user info
        if is_member(user, 'Merchant'):
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

            merchant_item_code = '{0:05}'.format(user.id)
            sales = Sales.objects.filter(item__startswith=merchant_item_code).order_by('-date')
            context_dict['sales'] = sales

            # Get Sales
            unpaid = 0
            for sale in sales:
                if not sale.payout:
                    unpaid = unpaid + sale.net
            context_dict['unpaid'] = unpaid

            payouts = Payout.objects.filter(merchant=user).order_by('-date')
            context_dict['payouts'] = payouts

            earnings = 0
            for payout in payouts:
                earnings = earnings + payout.amount
            context_dict['earnings'] = earnings
        else:
            raise PermissionDenied

    except PermissionDenied:
        logout(request)
        raise

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
def cube(request, cube_id):

    try:
        template = 'viewer_app/cube.html'
        context_dict = dict()

        cube = Cube.objects.get(id=cube_id)
        context_dict['cube'] = cube

        items = Item.objects.filter(cube=cube)
        context_dict['items'] = items

    except ObjectDoesNotExist:
        raise Http404

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
def item(request, item_id):

    try:
        template = 'viewer_app/item.html'
        context_dict = dict()

        item = Item.objects.get(id=item_id)
        context_dict['item'] = item

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required
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
        raise
        return server_error(request)

    return render(request, template, context_dict)

