from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error


from system_app.forms.bank import BankForm
from system_app.models import Bank

@login_required
def edit(request, bank_id):

    try:
        template = 'system_app/bank/edit.html'
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
