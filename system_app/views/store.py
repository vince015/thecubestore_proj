from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error


from system_app.forms.store import StoreForm
from system_app.models import Store
from util.util import SYSTEM_APP_LOGIN, is_crew

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def edit(request, store_id):

    try:
        template = 'system_app/store/edit.html'
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
