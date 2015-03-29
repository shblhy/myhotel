# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.order import views 

urlpatterns = patterns('',
    url(r'^orders$', views.orders, name='admin_order_orders'),
    url(r'^orders\.(?P<contype>(html|table|csv))', views.orders, name="admin_order_orders_table"),
    #url(r'^add_order.*$','order.views.add_order'),
    #url(r'^add$','order.views.order_input'),
    url(r'^add/(?P<room_type>[\d]+)$', views.order_input),
    #url(r'^delete$','order.views.delete_orders'),
    #url(r'^edit/(?P<order_id>[\d]+)$','order.views.order_input',{'action':'edit'}),
    url(r'^input_order', views.input_order),
    #url(r'^edit_order$','order.views.input_order',{'action':'edit'}),
    #url(r'^user/edit/(?P<user_id>[\d]+)$','member.views_user.user_input',{'action':'edit'},name="admin_user_input"),
    #url(r'^import_orders$','member.views.import_orders'),
    url(r'^delete_orders$', views.delete_orders),
)
