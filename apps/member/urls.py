# -*- coding: utf-8 -*-
from django.conf.urls import patterns,  url
from apps.member import views, views_user, views_group

urlpatterns = patterns('',
        #-------------------------访客--------------------------------------------
        url(r'^login_page/$', views.login_page, name='login'),
        url(r'^regist_page/$', views.regist_page, name='regist'),
        url(r'^login/$', views.login, name='action_login'),
        #-------------------------登录用户--------------------------------------------
        url(r'^logout/$', views.logout, name='action_logout'),
        url(r'^password_change/$', views.password_change),
        url(r'^password_change/done/$', views.password_change_done),
        url(r'^center$', views_user.user_center, name="user_center"),
        #-------------------------管理员管理用户--------------------------------------------
        url(r'^users$', views_user.users,name="admin_member_users"),
        url(r'^users\.(?P<contype>(html|table|csv))', views_user.users, name="admin_member_users_table"),
        url(r'^user/add$',views_user.user_input, name="admin_user_add"),
        url(r'^user/edit/(?P<user_id>[\d]+)$', views_user.user_input, name="admin_user_input"),
        url(r'^user/detail/(?P<user_id>[\d]+)$', views_user.user_detail, name="admin_user_detail"),
        url(r'^input_user$', views_user.input_user, name="admin_user_input_action"),
        url(r'^regist/$', views_user.regist, name="admin_user_input_action"),
        url(r'^add_user$', views_user.input_user, name="admin_user_add_action"),
        url(r'^edit_user$', views_user.input_user, name="admin_user_edit_action"),
        url(r'^import_users$', views_user.import_users, name="admin_user_import"),
        url(r'^delete_users', views_user.delete_users, name="admin_user_delete"),
        url(r'^groups$', views_group.groups),
        url(r'^groups.?(?P<contype>(table|csv))$', views_group.groups),

    )