# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.room import views, views_room_type

urlpatterns = patterns('',
    url(r'^rooms$', views.rooms, name='admin_room'),
    url(r'^rooms.?(?P<contype>(page|table|csv))$', views.rooms),
    url(r'^add$', views.room_input, name='admin_room_add'),
    url(r'^edit/(?P<room_id>[\d]+)$', views.room_input),
    url(r'^detail/(?P<room_id>[\d]+)$', views.room_detail),
    url(r'^add_room$', views.input_room),
    url(r'^edit_room$', views.input_room),
    url(r'^import_rooms$', views.import_rooms),
    url(r'^delete_rooms$', views.delete_rooms),
    url(r'^room_types$', views_room_type.room_types, name='admin_room_types'),
    url(r'^room_types\.(?P<contype>(html|table|csv))', views_room_type.room_types, name="admin_room_types_table"),
    url(r'^room_type/add$', views_room_type.room_type_input),
    url(r'^room_type/edit/(?P<room_type_id>[\d]+)$', views_room_type.room_type_input),
    url(r'^room_type/detail/(?P<room_type_id>[\d]+)$', views_room_type.room_type_detail),
    url(r'^room_type/add_room_type$', views_room_type.input_room_type),
    url(r'^room_type/edit_room_type$', views_room_type.input_room_type),
    url(r'^room_type/upload_photo$', views_room_type.upload_photo),
    url(r'^delete_room_types$', views_room_type.delete_room_types),
)
