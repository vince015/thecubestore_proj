from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from system_app.views import home, merchant, cube, item, payout, sales, announcement

home_url = [
    url(r'^login/$', home.user_login, name='login'),
    url(r'^logout/$', home.user_logout, name='logout'),
    url(r'^dashboard/$', home.dashboard, name='dashboard'),
    url(r'^search/$', home.search, name='search'),
    url(r'^buy/(?P<item_id>[0-9]+)$', home.buy, name='buy')
]

merchant_url = [
    url(r'^merchant/(?P<user_id>[0-9]+)$', merchant.detail, name='merchant_detail'),
    url(r'^merchant/all/$', merchant.all, name='merchant_all'),
    url(r'^merchant/add/$', merchant.add, name='merchant_add'),
    url(r'^merchant/password/$', merchant.change_password, name='change_password'),
    url(r'^merchant/profile/(?P<profile_id>\w+)$', merchant.profile_edit, name='profile_edit'),
    url(r'^merchant/contact/(?P<contact_id>[0-9]+)$', merchant.contact_edit, name='contact_edit'),
    url(r'^merchant/store/(?P<store_id>[0-9]+)$', merchant.store_edit, name='store_edit'),
    url(r'^merchant/bank/(?P<bank_id>[0-9]+)$', merchant.bank_edit, name='bank_edit'),
    url(r'^merchant/delete/(?P<user_id>[0-9]+)$', merchant.delete, name='merchant_delete'),
    url(r'^merchant/json$', login_required(merchant.MerchantsListJson.as_view()), name='merchants_json'),
    url(r'^merchant/cube/json/(?P<user_id>[0-9]+)$', login_required(merchant.MerchantsCubeJson.as_view()), name='merchants_cube_json'),
    url(r'^merchant/payout/json/(?P<user_id>[0-9]+)$', login_required(merchant.MerchantsPayoutJson.as_view()), name='merchants_payout_json'),
    url(r'^merchant/sale/json/(?P<user_id>[0-9]+)$', login_required(merchant.MerchantsSalesJson.as_view()), name='merchants_sale_json')
]

cube_url = [
    url(r'^cube/(?P<cube_id>[0-9]+)$', cube.detail, name='cube_detail'),
    url(r'^cube/all/$', cube.all, name='cube_all'),
    url(r'^cube/add/(?P<user_id>[0-9]+)$', cube.add, name='cube_add'),
    url(r'^cube/edit/(?P<cube_id>[0-9]+)$', cube.edit, name='cube_edit'),
    url(r'^cube/delete/(?P<cube_id>[0-9]+)$', cube.delete, name='cube_delete'),
    url(r'^cube/json$', login_required(cube.CubesListJson.as_view()), name='cubes_json'),
    url(r'^cube/items/json/(?P<cube_id>[0-9]+)$', login_required(cube.CubesItemJson.as_view()), name='cubes_item_json')
]

item_url = [
    url(r'^item/(?P<item_id>[0-9]+)$', item.detail, name='item_detail'),
    url(r'^item/all/$', item.all, name='item_all'),
    url(r'^item/add/(?P<cube_id>[0-9]+)$', item.add, name='item_add'),
    url(r'^item/edit/(?P<item_id>[0-9]+)$', item.edit, name='item_edit'),
    url(r'^item/delete/(?P<item_id>[0-9]+)$', item.delete, name='item_delete'),
    url(r'^item/inventory/(?P<cube_id>[0-9]+)$', item.inventory, name='item_inventory'),
    url(r'^item/json/$', login_required(item.ItemsListJson.as_view()), name='items_json')
]

payout_url = [
    url(r'^payout/(?P<payout_id>[0-9]+)$', payout.detail, name='payout_detail'),
    url(r'^payout/all/$', payout.all, name='payout_all'),
    url(r'^payout/add/(?P<user_id>[0-9]+)$', payout.add, name='payout_add'),
    url(r'^payout/edit/(?P<payout_id>[0-9]+)$', payout.edit, name='payout_edit'),
    url(r'^payout/delete/(?P<payout_id>[0-9]+)$', payout.delete, name='payout_delete'),
    url(r'^payout/json/$', login_required(payout.PayoutsListJson.as_view()), name='payouts_json'),
    url(r'^payout/sales/json/(?P<payout_id>[0-9]+)$', login_required(payout.PayoutSalesJson.as_view()), name='payout_sales_json')
]

sales_url = [
    url(r'^sales/add/$', sales.add, name='sales_add'),
    url(r'^sales/pay/(?P<payout_id>[0-9]+)$', sales.pay, name='sales_pay'),
    url(r'^sales/all/$', sales.all, name='sales_all'),
    url(r'^sales/json$', login_required(sales.SalesListJson.as_view()), name='sales_json'),
    url(r'^sales/unpaid/json$', login_required(sales.SalesPayJson.as_view()), name='sales_pay_json')
]

announcement_url = [
    url(r'^announcement/(?P<announcement_id>[0-9]+)$', announcement.detail, name='announcement_detail'),
    url(r'^announcement/all/$', announcement.all, name='announcement_all'),
    url(r'^announcement/add/$', announcement.add, name='announcement_add'),
    url(r'^announcement/edit/(?P<announcement_id>[0-9]+)$', announcement.edit, name='announcement_edit'),
    url(r'^announcement/delete/(?P<announcement_id>[0-9]+)$', announcement.delete, name='announcement_delete')
]

urlpatterns = home_url + merchant_url + cube_url + item_url + payout_url + sales_url + announcement_url