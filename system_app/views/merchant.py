from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms.models import model_to_dict

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error


from system_app.forms.merchant import MerchantForm, ContactForm, StoreForm, BankForm, ProfileForm
from system_app.models import Contact, Store, Bank, Cube, Payout, Sales, Profile

@login_required
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

        cubes = Cube.objects.filter(user=user).order_by('-next_due_date')
        context_dict['cubes'] = cubes

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
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
def all(request):

    try:
        template = 'system_app/merchant/all.html'
        context_dict = dict()
        context_dict['merchants'] = list()

        users = User.objects.filter(groups__name='Merchant')
        for user in users:
            cubes = Cube.objects.filter(user=user)
            profile = Profile.objects.get(user=user)

            profile_dict = model_to_dict(profile)
            profile_dict.update(model_to_dict(user))

            context_dict['merchants'].append({'profile': profile_dict,
                                              'cubes': cubes})

    except ObjectDoesNotExist:
        raise Http404

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
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

@login_required
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
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
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
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
def contact_edit(request, contact_id):

    try:
        template = 'system_app/merchant/contact_edit.html'
        context_dict = dict()

        instance = Contact.objects.get(id=contact_id)

        if request.method == "POST":
            form = ContactForm(request.POST, instance=instance)
            context_dict['form'] = form

            if form.is_valid():
                contact = form.save(commit=False)
                contact.save()

                messages.success(request, 'Successfully edited contact.')

                return redirect('/system/merchant/{0}'.format(contact.user.id))
        else:
            form = ContactForm(instance=instance)
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
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
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
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
        raise
        return server_error(request)

    return render(request, template, context_dict)

