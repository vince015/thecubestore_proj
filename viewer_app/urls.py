from django.conf.urls import url
from viewer_app import views

urlpatterns = [
    url(r'^login/$', views.user_login, name='viewer_login'),
    url(r'^logout/$', views.user_logout, name='viewer_logout'),
    url(r'^change_password/$', views.change_password, name='viewer_change_password'),
    url(r'^$', views.profile, name='profile'),

    url(r'^cube/(?P<cube_id>[0-9]+)$', views.cube, name='view_cube'),
    url(r'^item/(?P<item_id>[0-9]+)$', views.item, name='view_item'),
    url(r'^payout/(?P<payout_id>[0-9]+)$', views.payout, name='view_payout')
]