# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.order import views 

urlpatterns = patterns('',
    #---------------customer---------------------------------------------------
    url(r'^detail/(?P<order_id>[\d]+)$', views.order_detail),
    url(r'^add/(?P<room_type>[\d]+)$', views.order_input),
    url(r'^input_order', views.input_order),
    #---------------hotel manager---------------------------------------------------
    url(r'^orders$', views.orders, name='admin_order_orders'),
    url(r'^orders\.(?P<contype>(html|table|csv))', views.orders, name="admin_order_orders_table"),
    url(r'^admin/delete_orders$', views.delete_orders),
    url(r'^admin/detail/(?P<order_id>[\d]+)$', views.order_detail_admin),

)
