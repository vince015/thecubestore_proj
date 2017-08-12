from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error


from system_app.models import Sales, Item, Payout

def compute_net(amount, vat, sales):

    vat_deduct = amount * (vat / 100)
    sales_deduct = amount * (sales / 100)
    return amount - vat_deduct - sales_deduct

def current_date():

    try:
        now = datetime.utcnow()
        # Add 8hrs for PH time
        pst = now + timedelta(hours=8)
        formatted = datetime.strftime(pst, '%Y-%m-%d')
        return formatted

    except:
        raise

@login_required
def add(request):

    try:

        if request.method == "POST":
            item = Item.objects.get(id=request.POST.get('item'))

            quantity = int(request.POST.get('quantity'))
            gross = item.price*quantity
            net = compute_net(gross, item.vat, item.commission)
            sales = Sales.objects.create(item=item.code,
                                         date=current_date(),
                                         quantity=quantity,
                                         net=net,
                                         gross=gross,
                                         payout=None)

            item.quantity = item.quantity - quantity
            item.save()

            return redirect('/system/dashboard')
        else:
            raise Exception('Invalid method')

    except:
        return server_error(request)


@login_required
def pay(request, payout_id):

    try:
        template = 'system_app/sales/pay.html'
        context_dict = dict()

        # Get user object
        payout = Payout.objects.get(id=payout_id)
        context_dict['payout'] = payout

        sales = Sales.objects.filter(payout=None).order_by('-date')
        context_dict['sales'] = sales
        if request.method == "POST":
            selected_sales = request.POST.getlist('sales')
            for sale_id in selected_sales:
                selected_sale = Sales.objects.get(id=int(sale_id))
                selected_sale.payout = payout.id
                selected_sale.save()

            return redirect('/system/payout/{0}'.format(payout.id))

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)