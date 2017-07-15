from django.conf.urls import url
from system_app.views import home, merchant

home_url = [
    url(r'^login/$', home.user_login, name='login'),
    url(r'^logout/$', home.user_logout, name='logout'),
    url(r'^$', home.dashboard, name='dashboard')
]

merchant_url = [
    url(r'^merchant/add/$', merchant.add, name='merchant_add')
]

urlpatterns = home_url + merchant_url