from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
from django.views.defaults import server_error
from django_datatables_view.base_datatable_view import BaseDatatableView


from system_app.forms.item import ItemForm
from system_app.models import Cube, Item
from util.util import SYSTEM_APP_LOGIN, is_crew


class ItemsListJson(BaseDatatableView):
    model = Item
    columns = ['code', 'description', 'quantity', 'price', 'cube']
    order_columns = ['code', 'description', 'quantity', 'price', 'cube.unit']

    def get_initial_queryset(self):
        return Item.objects.all()

    def render_column(self, row, column):
        if column == 'code':
            link = '<a href="/system/item/{0}">{1}</a>'.format(row.id, row.code)
            return link
        elif column == 'cube':
            link = '<a href="/system/cube/{0}">{1}</a>'.format(row.cube.id, row.cube.unit)
            return link
        else:
            return super(ItemsListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(description__icontains=search) |
                           Q(code__icontains=search) |
                           Q(cube__unit__icontains=search))
        return qs

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def detail(request, item_id):

    try:
        template = 'system_app/item/detail.html'
        context_dict = dict()

        item = Item.objects.get(id=item_id)
        context_dict['item'] = item

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def all(request):

    try:
        template = 'system_app/item/all.html'
        context_dict = dict()

        items = Item.objects.all()
        context_dict['items'] = items

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def add(request, cube_id):

    try:
        template = 'system_app/item/add.html'
        context_dict = dict()

        # Get cube object
        cube = Cube.objects.get(id=cube_id)
        context_dict['cube'] = cube

        if request.method == "POST":
            form = ItemForm(request.POST)
            context_dict['form'] = form

            if form.is_valid():
                item = form.save(commit=False)
                item.cube = cube
                item.save()

                messages.success(request, 'Successfully added item.')

                return redirect('/system/item/{0}'.format(item.id))
        else:
            form = ItemForm()
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def edit(request, item_id):

    try:
        template = 'system_app/item/edit.html'
        context_dict = dict()

        instance = Item.objects.get(id=item_id)

        if request.method == "POST":
            form = ItemForm(request.POST, instance=instance)
            context_dict['form'] = form

            if form.is_valid():
                item = form.save(commit=False)
                item.save()

                messages.success(request, 'Successfully edited item.')

                return redirect('/system/item/{0}'.format(item.id))
        else:
            form = ItemForm(instance=instance)
            context_dict['form'] = form

    except ObjectDoesNotExist:
        raise Http404

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def delete(request, item_id):

    try:
        template = 'system_app/item/delete.html'
        context_dict = dict()

        item = Item.objects.get(id=item_id)
        context_dict['item'] = item

        if request.method == "POST":
            item.delete()

            messages.success(request, 'Successfully deleted item.')

            return redirect('/system/item/all')

    except ObjectDoesNotExist:
        raise Http404()

    except:
        return server_error(request)

    return render(request, template, context_dict)

@login_required(login_url=SYSTEM_APP_LOGIN)
@user_passes_test(is_crew, login_url=SYSTEM_APP_LOGIN)
def inventory(request, cube_id):

    try:
        if request.method == "POST":
            for item in request.POST:
                # format: __<item.id>_<item.code>_<type>' e.g.'__1_A1-0001_out'
                if item.startswith('__'):
                    splits = item.split('_')
                    target_item = Item.objects.get(id=int(splits[2]),
                                                   code=splits[3])
                    # print('{0} => {1}'.format(item, request.POST.get(item)))
                    if splits[-1] == 'in':
                        val = int(request.POST.get(item))
                        target_item.quantity = target_item.quantity + val
                    elif splits[-1] == 'out':
                        val = int(request.POST.get(item))
                        target_item.quantity = target_item.quantity - val
                    elif splits[-1] == 'price':
                        val = float(request.POST.get(item))
                        target_item.price = val
                    target_item.save()

            messages.success(request, 'Successfully updates inventory.')

            return redirect('/system/cube/{0}#cube-item'.format(cube_id))

    except ObjectDoesNotExist:
        raise Http404()

    except:
        raise
        return server_error(request)

    return render(request, template, context_dict)
