from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render

from django.views.defaults import server_error


from system_app.forms.merchant import MerchantForm
from system_app.models import Contact, Store, Bank

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

                    return render(request, 'placeholder.html', context_dict)
                else:
                    form.add_error('username', 'Username already used.')
        else:
            form = MerchantForm()
            context_dict['form'] = form

    except:
        return server_error(request)

    return render(request, template, context_dict)
