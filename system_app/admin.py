from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from system_app.models import Contact, Store, Bank, Cube, Item, Payout, Sales
from django.core import urlresolvers

from import_export import resources


class ContactResource(resources.ModelResource):

    class Meta:
        model = Contact
        fields = ('user__first_name', 'user__last_name', 'user__email', 'contact_number')

class ContactAdmin(ImportExportModelAdmin):
    list_display = ('id', 'merchant', 'contact_number', 'primary_address', 'alternate_address')
    list_display_links = ['id']
    search_fields = ('id', 'contact_number')
    list_per_page = 50
    resource_class = ContactResource

    def merchant(self, obj):
        link = urlresolvers.reverse("admin:auth_user_change", args=[obj.user.id]) #model name has to be lowercase
        return '<a href="{0}">{1} {2}</a>'.format(link, obj.user.first_name, obj.user.last_name)
    merchant.allow_tags = True

admin.site.register(Contact, ContactAdmin)

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'merchant', 'name', 'product', 'facebook', 'instagram', 'website')
    list_display_links = ['id']
    search_fields = ('id', 'name')
    list_per_page = 50

    def merchant(self, obj):
        link = urlresolvers.reverse("admin:auth_user_change", args=[obj.user.id]) #model name has to be lowercase
        return '<a href="{0}">{1} {2}</a>'.format(link, obj.user.first_name, obj.user.last_name)
    merchant.allow_tags = True

admin.site.register(Store, StoreAdmin)

class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'merchant', 'owner', 'bank', 'account')
    list_display_links = ['id']
    search_fields = ('id', 'owner', 'bank', 'account')
    list_per_page = 50

    def merchant(self, obj):
        link = urlresolvers.reverse("admin:auth_user_change", args=[obj.user.id]) #model name has to be lowercase
        return '<a href="{0}">{1} {2}</a>'.format(link, obj.user.first_name, obj.user.last_name)
    merchant.allow_tags = True

admin.site.register(Bank, BankAdmin)

class CubeAdmin(admin.ModelAdmin):
    list_display = ('id', 'merchant', 'unit', 'duration', 'promo', 'start_date', 'end_date', 'next_due_date')
    list_display_links = ['id']
    search_fields = ('unit', 'duration', 'promo', 'start_date', 'end_date', 'next_due_date')
    list_per_page = 50

    def merchant(self, obj):
        link = urlresolvers.reverse("admin:auth_user_change", args=[obj.user.id]) #model name has to be lowercase
        return '<a href="{0}">{1} {2}</a>'.format(link, obj.user.first_name, obj.user.last_name)
    merchant.allow_tags = True

admin.site.register(Cube, CubeAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'containing_cube', 'quantity', 'price', 'vat', 'commission', 'description')
    list_display_links = ['code']
    search_fields = ['code']
    list_per_page = 50

    def containing_cube(self, obj):
        link = urlresolvers.reverse("admin:system_app_cube_change", args=[obj.cube.id]) #model name has to be lowercase
        return '<a href="{0}">{1}</a>'.format(link, obj.cube.unit)
    containing_cube.allow_tags = True

admin.site.register(Item, ItemAdmin)

class PayoutResource(resources.ModelResource):

    class Meta:
        model = Payout
        fields = ('id', 'bank__bank', 'bank__account', 'bank__owner', 'date', 'amount')

class PayoutAdmin(ImportExportModelAdmin):
    list_display = ('id', 'merchant', 'bank_account', 'date', 'amount')
    list_display_links = ['id']
    search_fields = ['id']
    list_per_page = 50
    resource_class = PayoutResource

    def merchant(self, obj):
        link = urlresolvers.reverse("admin:auth_user_change", args=[obj.user.id]) #model name has to be lowercase
        return '<a href="{0}">{1} {2}</a>'.format(link, obj.user.first_name, obj.user.last_name)
    merchant.allow_tags = True

    def bank_account(self, obj):
        link = urlresolvers.reverse("admin:system_app_bank_change", args=[obj.bank.id]) #model name has to be lowercase
        return '<a href="{0}">{1} ({2})</a>'.format(link, obj.bank.bank, obj.bank.account)
    bank_account.allow_tags = True

admin.site.register(Payout, PayoutAdmin)

class SalesResource(resources.ModelResource):

    class Meta:
        model = Sales
        fields = ('id', 'item', 'quantity', 'date', 'gross', 'net', 'payout')

class SalesAdmin(ImportExportModelAdmin):
    list_display = ('id', 'item', 'quantity', 'date', 'gross', 'net', 'payout')
    search_fields = ['id']
    list_per_page = 50
    resource_class = SalesResource

admin.site.register(Sales, SalesAdmin)
