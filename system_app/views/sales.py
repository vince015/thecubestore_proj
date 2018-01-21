from decimal import Decimal
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error
from django_datatables_view.base_datatable_view import BaseDatatableView


from system_app.models import Sales, Item, Payout
from util.util import SYSTEM_APP_LOGIN, is_crew

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

class SalesListJson(BaseDatatableView):
    model = Sales
    columns = ['item', 'date', 'quantity', 'gross', 'payout']
    order_columns = ['item', 'date', 'quantity', 'gross', 'payout']

    def get_initial_queryset(self):
        return Sales.objects.all()

    def render_column(self, row, column):
        if column == 'item':
            link = row.item
            item = Item.objects.filter(code=row.item).first()
            if item:
                link = '<a href="/system/item/{0}">{1}</a>'.format(item.id, item.code)
            return link
        elif column == 'payout':
            link = '<small class="label label-danger">Unpaid</small>'
            if row.payout:
                payout = Payout.objects.filter(id=row.payout).first()
                if payout:
                    link = '<small class="label label-default"><a href="/system/payout/{0}">{1}</a></small>'.format(payout.id, payout.id)
                else:
                    link = '<small class="label label-warning">{0}</small>'.format(row.payout)
            return link
        else:
            return super(SalesListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(item__icontains=search) |
                           Q(date__icontains=search) |
                           Q(payout__icontains=search))
        return qs

class SalesPayJson(BaseDatatableView):
    model = Sales
    columns = ['action', 'item', 'date', 'quantity', 'gross', 'net']
    order_columns = ['item', 'item', 'date', 'quantity', 'gross', 'net']

    def get_initial_queryset(self):
        return Sales.objects.filter(payout=None)

    def render_column(self, row, column):
        if column == 'action':
            html = '<input type="checkbox" name="sales" value="{0}">'.format(row.id)
            return html
        else:
            return super(SalesPayJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(item__icontains=search) |
                           Q(date__icontains=search) |
                           Q(payout__icontains=search))
        return qs

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def all(request):

    try:
        template = 'system_app/sales/all.html'

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def add(request):

    try:

        if request.method == "POST":
            item = Item.objects.get(id=request.POST.get('item'))

            quantity = int(request.POST.get('quantity'))
            discount = Decimal(request.POST.get('discount')) * Decimal(0.01)
            new_price = item.price - (item.price * discount)

            gross = new_price * quantity
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
        raise
        # return server_error(request)


@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
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
        # raise
        return server_error(request)

    return render(request, template, context_dict)
