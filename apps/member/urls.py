# -*- coding: utf-8 -*-
from django.conf.urls import patterns,  url

urlpatterns = patterns('',
        #-------------------------访客--------------------------------------------
        url(r'^login_page/$', 'member.views.login_page',name='login'),
        url(r'^regist_page/$', 'member.views.regist_page',name='regist'),
        url(r'^login/$', 'member.views.login',name='action_login'),
        #-------------------------登录用户--------------------------------------------
        url(r'^logout/$', 'member.views.logout',name='action_logout'),
        url(r'^password_change/$', 'member.views.password_change'),
        url(r'^password_change/done/$', 'member.views.password_change_done'),
        url(r'^center$','member.views_user.user_center',name="user_center"),
        #-------------------------管理员管理用户--------------------------------------------
        url(r'^users$','member.views_user.users',name="admin_member_users"),
        url(r'^users\.(?P<contype>(html|table|csv))', 'member.views_user.users', name="admin_member_users_table"),
        #url(r'^users.?(?P<contype>(table|csv))$', 'member.views_user.users',name="admin_member_users_table"),
        url(r'^user/add$','member.views_user.user_input',{'action':'add'},name="admin_user_add"),
        url(r'^user/edit/(?P<user_id>[\d]+)$','member.views_user.user_input',{'action':'edit'},name="admin_user_input"),
        url(r'^user/detail/(?P<user_id>[\d]+)$','member.views_user.user_detail',name="admin_user_detail"),
        url(r'^input_user$','member.views_user.input_user',name="admin_user_input_action"),
        url(r'^regist/$','member.views_user.regist',name="admin_user_input_action"),
        url(r'^add_user$','member.views_user.input_user',{'action':'add'},name="admin_user_add_action"),
        url(r'^edit_user$','member.views_user.input_user',{'action':'edit'},name="admin_user_edit_action"),
        url(r'^import_users$','member.views_user.import_users',name="admin_user_import"),
        url(r'^delete_users','member.views_user.delete_users',name="admin_user_delete"),
        url(r'^groups$','member.views_group.groups'),
        url(r'^groups.?(?P<contype>(table|csv))$', 'member.views_group.groups'),

    )