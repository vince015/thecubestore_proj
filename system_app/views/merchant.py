from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms.models import model_to_dict
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error
from django_datatables_view.base_datatable_view import BaseDatatableView


from system_app.forms.merchant import MerchantForm, ContactForm, UserEditForm, StoreForm, BankForm, ProfileForm
from system_app.models import Contact, Store, Bank, Cube, Payout, Sales, Profile, Item
from util.util import SYSTEM_APP_LOGIN, is_crew


class MerchantsListJson(BaseDatatableView):
    model = Profile
    columns = ['merchant_id', 'name', 'unpaid sales', 'cubes']
    order_columns = ['merchant_id', 'user.first_name']

    def get_initial_queryset(self):
        return Profile.objects.all()

    def render_column(self, row, column):
        if column == 'merchant_id':
            link = '<a href="/system/merchant/{0}">{1}</a>'.format(row.user.id, row.merchant_id)
            return link
        elif column == 'name':
            link = '{0} {1}'.format(row.user.first_name, row.user.last_name)
            return link
        elif column == 'cubes':
            cubes = Cube.objects.filter(user=row.user)

            html = ''
            for cube in cubes:
                html = html + '<small class="label label-default"><a href="/system/cube/{0}">{1}</a></small>&nbsp;'.format(cube.id, cube.unit)
            return html
        elif column == 'unpaid sales':
            sales = Sales.objects.filter(item__startswith=row.merchant_id)

            unpaid = 0
            for sale in sales:
                if not sale.payout:
                    unpaid = unpaid + sale.net
            return unpaid
        else:
            return super(MerchantsListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(merchant_id__icontains=search) |
                           Q(user__first_name__icontains=search) |
                           Q(user__last_name__icontains=search))
        return qs

class MerchantsCubeJson(BaseDatatableView):
    model = Cube
    columns = ['unit', 'next_due_date', 'rate', 'action']
    order_columns = ['unit', 'next_due_date', 'rate']

    def get_initial_queryset(self, **kwargs):
        user_id = self.kwargs.get('user_id')
        return Cube.objects.filter(user=user_id)

    def render_column(self, row, column):
        if column == 'unit':
            link = '<a href="/system/cube/{0}">{1}</a>'.format(row.id, row.unit)
            return link
        elif column == 'action':
            html = '<a href="/system/cube/edit/{0}" class="pull-right"><i class="fa fa-pencil"></i></a>'.format(row.id)
            return html
        else:
            return super(MerchantsCubeJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(unit__icontains=search) |
                           Q(next_due_date__icontains=search))
        return qs

class MerchantsPayoutJson(BaseDatatableView):
    model = Payout
    columns = ['reference_number', 'date', 'amount', 'action']
    order_columns = ['reference_number', 'date', 'amount', 'action']

    def get_initial_queryset(self, **kwargs):
        user_id = self.kwargs.get('user_id')
        return Payout.objects.filter(merchant=user_id)

    def render_column(self, row, column):
        if column == 'id':
            link = '<a href="/system/payout/{0}">{1}</a>'.format(row.id, row.reference_number)
            return link
        elif column == 'action':
            html = '<a href="/system/payout/edit/{0}" class="pull-right"><i class="fa fa-pencil"></i></a>'.format(row.id)
            return html
        else:
            return super(MerchantsPayoutJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(reference_number__icontains=search) |
                           Q(date__icontains=search))
        return qs

class MerchantsSalesJson(BaseDatatableView):
    model = Sales
    columns = ['item', 'date', 'quantity', 'gross', 'net', 'payout']
    order_columns = ['item', 'date', 'quantity', 'gross', 'net', 'payout']

    def get_initial_queryset(self, **kwargs):
        user_id = self.kwargs.get('user_id')
        profile = Profile.objects.get(user=user_id)
        return Sales.objects.filter(item__startswith=profile.merchant_id)

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
            return super(MerchantsSalesJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(item__icontains=search) |
                           Q(date__icontains=search) |
                           Q(payout__icontains=search))
        return qs

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def detail(request, user_id):

    try:
        template = 'system_app/merchant/detail.html'
        context_dict = dict()

        user = User.objects.get(id=user_id)
        context_dict['profile'] = user.__dict__

        profile = Profile.objects.filter(user=user).first()
        if profile:
            context_dict['profile'].update(profile.__dict__)
            form = ProfileForm(instance=profile)
            context_dict['form'] = form

            sales = Sales.objects.filter(item__startswith=profile.merchant_id).order_by('-date')
            context_dict['sales'] = sales

        contact = Contact.objects.filter(user=user).first()
        if contact:
            context_dict['contact'] = contact

        store = Store.objects.filter(user=user).first()
        if store:
            context_dict['store'] = store

        bank = Bank.objects.filter(user=user).first()
        if bank:
            context_dict['bank']  = bank

        payouts = Payout.objects.filter(merchant=user).order_by('-date')
        context_dict['payouts'] = payouts

        # Get Sales
        unpaid = 0
        for sale in sales:
            if not sale.payout:
                unpaid = unpaid + sale.net
        context_dict['unpaid'] = unpaid

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def all(request):

    try:
        template = 'system_app/merchant/all.html'

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def add(request):

    try:
        template = 'system_app/merchant/add.html'
        context_dict = dict()

        if request.method == "POST":
            form = MerchantForm(request.POST)
            context_dict['form'] = form

            if form.is_valid():
                user, created = User.objects.get_or_create(username=form.cleaned_data.get('username'))

                if created:
                    user.set_password(form.cleaned_data.get('password'))
                    user.email = form.cleaned_data.get('email')
                    user.first_name = form.cleaned_data.get('firstname')
                    user.last_name = form.cleaned_data.get('lastname')
                    user.save()

                    # Add to group
                    group = Group.objects.get(name='Merchant')
                    group.user_set.add(user)

                    Profile.objects.create(user=user,
                                           merchant_id=form.cleaned_data.get('merchant_id'),
                                           remarks=form.cleaned_data.get('remarks'))

                    Contact.objects.create(user=user,
                                           contact_number=form.cleaned_data.get('contact_number'),
                                           primary_address=form.cleaned_data.get('primary_address'),
                                           alternate_address=form.cleaned_data.get('alternate_address'))

                    Store.objects.create(user=user,
                                         name=form.cleaned_data.get('storename'),
                                         product=form.cleaned_data.get('product'),
                                         facebook=form.cleaned_data.get('facebook'),
                                         instagram=form.cleaned_data.get('instagram'),
                                         website=form.cleaned_data.get('website'))

                    Bank.objects.create(user=user,
                                        owner=form.cleaned_data.get('bank_owner'),
                                        bank=form.cleaned_data.get('bank_name'),
                                        account=form.cleaned_data.get('bank_account'))

                    messages.success(request, 'Successfully added merchant.')

                    return redirect('/system/merchant/{0}'.format(user.id))
                else:
                    form.add_error('username', 'Username already used.')
        else:
            form = MerchantForm()
            context_dict['form'] = form

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def change_password(request):

    try:
        template = 'system_app/merchant/password.html'
        context_dict = dict()

        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            context_dict['form'] = form

            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')

                return redirect('/system/dashboard')
        else:
            form = PasswordChangeForm(request.user)
            context_dict['form'] = form

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def profile_edit(request, profile_id):

    try:
        template = 'system_app/merchant/profile_edit.html'
        context_dict = dict()

        instance = Profile.objects.get(pk=profile_id)

        if request.method == "POST":
            form = ProfileForm(request.POST, instance=instance)
            context_dict['form'] = form

            if form.is_valid():
                profile = form.save(commit=False)
                profile.save()

                messages.success(request, 'Successfully edited profile.')

                return redirect('/system/merchant/{0}'.format(profile.user.id))
        else:
            form = ProfileForm(instance=instance)
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def contact_edit(request, contact_id):

    try:
        template = 'system_app/merchant/contact_edit.html'
        context_dict = dict()

        instance = Contact.objects.get(id=contact_id)

        if request.method == "POST":
            form = ContactForm(request.POST, instance=instance)
            context_dict['form'] = form

            user_form = UserEditForm(request.POST, instance=instance.user)
            context_dict['user_form'] = user_form

            if form.is_valid() and user_form.is_valid():
                contact = form.save(commit=False)
                contact.user = user_form.save(commit=False)

                contact.user.save()
                contact.save()

                messages.success(request, 'Successfully edited contact.')

                return redirect('/system/merchant/{0}'.format(contact.user.id))
        else:
            form = ContactForm(instance=instance)
            context_dict['form'] = form

            user_form = UserEditForm(instance=instance.user)
            context_dict['user_form'] = user_form

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def store_edit(request, store_id):

    try:
        template = 'system_app/merchant/store_edit.html'
        context_dict = dict()

        instance = Store.objects.get(id=store_id)

        if request.method == "POST":
            form = StoreForm(request.POST, instance=instance)
            context_dict['form'] = form

            if form.is_valid():
                store = form.save(commit=False)
                store.save()

                messages.success(request, 'Successfully edited store.')

                return redirect('/system/merchant/{0}'.format(store.user.id))
        else:
            form = StoreForm(instance=instance)
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def bank_edit(request, bank_id):

    try:
        template = 'system_app/merchant/bank_edit.html'
        context_dict = dict()

        instance = Bank.objects.get(id=bank_id)

        if request.method == "POST":
            form = BankForm(request.POST, instance=instance)
            context_dict['form'] = form

            if form.is_valid():
                bank = form.save(commit=False)
                bank.save()

                messages.success(request, 'Successfully edited bank.')

                return redirect('/system/merchant/{0}'.format(bank.user.id))
        else:
            form = BankForm(instance=instance)
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def delete(request, user_id):

    try:
        user = User.objects.get(id=user_id)

        if request.method == "POST":
            user.delete()

            messages.success(request, 'Successfully deleted merchant.')

            return redirect('/system/merchant/all')

    except ObjectDoesNotExist:
        raise Http404()

    except:
        return server_error(request)

    return render(request, template, context_dict)
