# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^rooms$','room.views.rooms',name='admin_room'),
    url(r'^rooms.?(?P<contype>(page|table|csv))$', 'room.views.rooms'),
    
    
    #url(r'^brand/(?P<brand_id>[\d]+)/edit$', 'views_brand.brand_input', name="client_brand_edit"),#编辑或添加品牌的url
    #url(r'^brand/input_brand$', 'views_brand.input_brand', name="client_brand_action_input"),#编辑或添加品牌的url
    url(r'^add$','room.views.room_input',{'action':'add'},name='admin_room_add'),
    url(r'^edit/(?P<room_id>[\d]+)$','room.views.room_input',{'action':'edit'}),
    url(r'^detail/(?P<room_id>[\d]+)$','room.views.room_detail'),
    
    url(r'^add_room$','room.views.input_room',{'action':'add'}),
    url(r'^edit_room$','room.views.input_room',{'action':'edit'}),
    url(r'^import_rooms$','room.views.import_rooms'),
    url(r'^delete_rooms$','room.views.delete_rooms'),
    
    
    url(r'^room_types$','room.views_room_type.room_types',name='admin_room_types'),
    url(r'^room_types\.(?P<contype>(html|table|csv))', 'room.views_room_type.room_types', name="admin_room_types_table"),
    
    url(r'^room_type/add$','room.views_room_type.room_type_input',{'action':'add'}),
    url(r'^room_type/edit/(?P<room_type_id>[\d]+)$','room.views_room_type.room_type_input',{'action':'edit'}),
    url(r'^room_type/detail/(?P<room_type_id>[\d]+)$','room.views_room_type.room_type_detail'),
    
    url(r'^room_type/add_room_type$','room.views_room_type.input_room_type',{'action':'add'}),
    url(r'^room_type/edit_room_type$','room.views_room_type.input_room_type',{'action':'edit'}),
    url(r'^room_type/upload_photo$','room.views_room_type.upload_photo'),
)