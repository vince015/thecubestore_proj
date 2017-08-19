from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error


from system_app.forms.contact import ContactForm
from system_app.models import Contact
from util.util import SYSTEM_APP_LOGIN, is_crew

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def edit(request, contact_id):

    try:
        template = 'system_app/contact/edit.html'
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
