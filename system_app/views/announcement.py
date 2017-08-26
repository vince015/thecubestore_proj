from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error


from system_app.forms.announcement import AnnouncementForm
from system_app.models import Announcement
from util.util import SYSTEM_APP_LOGIN, is_crew

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def detail(request, announcement_id):

    try:
        template = 'system_app/announcement/detail.html'
        context_dict = dict()

        announcement = Announcement.objects.get(id=announcement_id)
        context_dict['announcement'] = announcement

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def all(request):

    try:
        template = 'system_app/announcement/all.html'
        context_dict = dict()

        announcements = Announcement.objects.all()
        context_dict['announcements'] = announcements

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def add(request):

    try:
        template = 'system_app/announcement/add.html'
        context_dict = dict()

        if request.method == "POST":
            form = AnnouncementForm(request.POST)
            context_dict['form'] = form

            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.save()

                messages.success(request, 'Successfully added announcement.')

                return redirect('/system/announcement/{0}'.format(announcement.id))
        else:
            form = AnnouncementForm()
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def edit(request, announcement_id):

    try:
        template = 'system_app/announcement/edit.html'
        context_dict = dict()

        instance = Announcement.objects.get(id=announcement_id)

        if request.method == "POST":
            form = AnnouncementForm(request.POST, instance=instance)
            context_dict['form'] = form

            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.save()

                messages.success(request, 'Successfully edited announcement.')

                return redirect('/system/announcement/{0}'.format(announcement.id))
        else:
            form = AnnouncementForm(instance=instance)
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def delete(request, announcement_id):

    try:
        template = 'system_app/announcement/delete.html'
        context_dict = dict()

        announcement = Announcement.objects.get(id=announcement_id)
        context_dict['announcement'] = announcement

        if request.method == "POST":
            announcement.delete()

            messages.success(request, 'Successfully deleted announcement.')

            return redirect('/system/announcement/all')

    except ObjectDoesNotExist:
        raise Http404()

    except:
        return server_error(request)

    return render(request, template, context_dict)
