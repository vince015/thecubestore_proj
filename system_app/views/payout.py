from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error


from system_app.forms.payout import PayoutForm
from system_app.models import Payout, Sales, Bank, Profile
from util.util import SYSTEM_APP_LOGIN, is_crew

def convert_date(str_time):

    try:
        date = datetime.strptime(str_time, '%m/%d/%Y')
        formatted = datetime.strftime(date, '%Y-%m-%d')
        return formatted

    except:
        raise

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def detail(request, payout_id):

    try:
        template = 'system_app/payout/detail.html'
        context_dict = dict()

        payout = Payout.objects.get(id=payout_id)
        context_dict['payout'] = payout

        sales = Sales.objects.filter(payout=payout.id)
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

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def all(request):

    try:
        template = 'system_app/payout/all.html'
        context_dict = dict()

        payouts = Payout.objects.all()
        context_dict['payouts'] = payouts

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def add(request, user_id):

    try:
        template = 'system_app/payout/add.html'
        context_dict = dict()

        # Get user object
        user = User.objects.get(id=user_id)
        context_dict['merchant'] = user

        profile = Profile.objects.get(user=user)
        sales = Sales.objects.filter(item__startswith=profile.merchant_id).filter(payout=None).order_by('-date')
        context_dict['sales'] = sales

        if request.method == "POST":
            form = PayoutForm(request.POST)
            context_dict['form'] = form

            if form.is_valid():
                payout = form.save(commit=False)
                payout.merchant = user

                bank = Bank.objects.filter(user=user).first()
                if bank:
                    payout.bank = bank

                payout.save()

                selected_sales = request.POST.getlist('sales')
                for sale_id in selected_sales:
                    selected_sale = Sales.objects.get(id=int(sale_id))
                    selected_sale.payout = payout.id
                    selected_sale.save()

                messages.success(request, 'Successfully added payout.')

                return redirect('/system/payout/{0}'.format(payout.id))
        else:
            form = PayoutForm()
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def edit(request, payout_id):

    try:
        template = 'system_app/payout/edit.html'
        context_dict = dict()

        instance = Payout.objects.get(id=payout_id)

        if request.method == "POST":
            form = PayoutForm(request.POST, instance=instance)
            context_dict['form'] = form

            if form.is_valid():
                payout = form.save(commit=False)
                payout.save()

                messages.success(request, 'Successfully edited payout.')

                return redirect('/system/payout/{0}'.format(payout.id))
        else:
            form = PayoutForm(instance=instance)
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def delete(request, payout_id):

    try:
        template = 'system_app/payout/delete.html'
        context_dict = dict()

        payout = Payout.objects.get(id=payout_id)
        context_dict['payout'] = payout

        if request.method == "POST":
            payout.delete()

            messages.success(request, 'Successfully deleted payout.')

            return redirect('/system/payout/all')

    except ObjectDoesNotExist:
        raise Http404()

    except:
        return server_error(request)

    return render(request, template, context_dict)
