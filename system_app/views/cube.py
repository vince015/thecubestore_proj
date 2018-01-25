from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error
from django_datatables_view.base_datatable_view import BaseDatatableView


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

class CubesListJson(BaseDatatableView):
    model = Cube
    columns = ['unit', 'next_due_date', 'start_date', 'end_date', 'rate', 'owner']
    order_columns = ['unit', 'next_due_date', 'start_date', 'end_date', 'rate', 'user.first_name']

    def get_initial_queryset(self):
        return Cube.objects.all()

    def render_column(self, row, column):
        if column == 'unit':
            link = '<a href="/system/cube/{0}">{1}</a>'.format(row.id, row.unit)
            return link
        elif column == 'owner':
            link = '<a href="/system/merchant/{0}">{1} {2}</a>'.format(row.user.id, row.user.first_name, row.user.last_name)
            return link
        else:
            return super(CubesListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(unit__icontains=search) |
                           Q(next_due_date__icontains=search) |
                           Q(start_date__icontains=search) |
                           Q(end_date__icontains=search) |
                           Q(user__first_name__icontains=search) |
                           Q(user__last_name__icontains=search))
        return qs

class CubesItemJson(BaseDatatableView):
    model = Item
    columns = ['code', 'description', 'quantity', 'price', 'in', 'out']
    order_columns = ['code', 'description', 'quantity']

    def get_initial_queryset(self, **kwargs):
        cube_id = self.kwargs.get('cube_id')
        return Item.objects.filter(cube=cube_id)

    def render_column(self, row, column):
        item = Item.objects.filter(code=row.code).first()
        if column == 'code':
            html = ''
            if item:
                html = '<a href="/system/item/{0}">{1}</a>'.format(item.id, item.code)
            return html
        elif column == 'price':
            if item:
                html = '<input type="number"\
                               name="__{0}_{1}_price"\
                               id="priceInput"\
                               min="1"\
                               step=0.01\
                               value="{2}"\
                               class="form-control pull-left"\
                               placeholder="Price"\
                               style="width: 100px">'.format(row.id, row.code, item.price)
            return html
        elif column == 'in':
            html = '<input type="number"\
                           name="__{0}_{1}_in"\
                           id="inInput"\
                           min="0"\
                           value="0"\
                           class="form-control pull-right"\
                           placeholder="In"\
                           style="width: 65px">'.format(row.id, row.code)
            return html
        elif column == 'out':
            link = '<input type="number"\
                           name="__{0}_{1}_out"\
                           id="outInput"\
                           max="{2}"\
                           min="0"\
                           value="0"\
                           class="form-control pull-right"\
                           placeholder="Out"\
                           style="width: 65px">'.format(row.id, row.code, row.quantity)
            return link
        else:
            return super(CubesItemJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(description__icontains=search) |
                           Q(code__icontains=search))
        return qs

@login_required(login_url=SYSTEM_APP_LOGIN)
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

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def all(request):

    try:
        template = 'system_app/cube/all.html'

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template)

@login_required(login_url=SYSTEM_APP_LOGIN)
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

@login_required(login_url=SYSTEM_APP_LOGIN)
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

@login_required(login_url=SYSTEM_APP_LOGIN)
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
