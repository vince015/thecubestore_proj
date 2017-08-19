from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error


from system_app.forms.cube import CubeForm
from system_app.models import Cube, Item
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
def detail(request, cube_id):

    try:
        template = 'system_app/cube/detail.html'
        context_dict = dict()

        cube = Cube.objects.get(id=cube_id)
        context_dict['cube'] = cube

        items = Item.objects.filter(cube=cube)
        context_dict['items'] = items

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def all(request):

    try:
        template = 'system_app/cube/all.html'
        context_dict = dict()

        cubes = Cube.objects.all()
        context_dict['cubes'] = cubes

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def add(request, user_id):

    try:
        template = 'system_app/cube/add.html'
        context_dict = dict()

        # Get user object
        user = User.objects.get(id=user_id)
        context_dict['merchant'] = user

        if request.method == "POST":
            form = CubeForm(request.POST)
            context_dict['form'] = form

            if form.is_valid():
                cube = form.save(commit=False)
                cube.user = user
                cube.save()

                messages.success(request, 'Successfully added cube.')

                return redirect('/system/cube/{0}'.format(cube.id))
        else:
            form = CubeForm()
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def edit(request, cube_id):

    try:
        template = 'system_app/cube/edit.html'
        context_dict = dict()

        instance = Cube.objects.get(id=cube_id)

        if request.method == "POST":
            form = CubeForm(request.POST, instance=instance)
            context_dict['form'] = form

            if form.is_valid():
                cube = form.save(commit=False)
                cube.save()

                messages.success(request, 'Successfully edited cube.')

                return redirect('/system/cube/{0}'.format(cube.id))
        else:
            form = CubeForm(instance=instance)
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def delete(request, cube_id):

    try:
        template = 'system_app/cube/delete.html'
        context_dict = dict()

        cube = Cube.objects.get(id=cube_id)
        context_dict['cube'] = cube

        if request.method == "POST":
            cube.delete()

            messages.success(request, 'Successfully deleted cube.')

            return redirect('/system/cube/all')

    except ObjectDoesNotExist:
        raise Http404()

    except:
        return server_error(request)

    return render(request, template, context_dict)
