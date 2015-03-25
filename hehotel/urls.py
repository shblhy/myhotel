# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from settings import RESOURCE_ROOT_PATH,STATIC_ROOT_PATH
from django.contrib import admin
from django.shortcuts import render_to_response
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hehotel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/$', 'hehotel.views.admin',name='admin'),  # 后台主页
    url(r'^$', 'hehotel.views.index', name='index'),
    url(r'^templates/(?P<path>.*)$', 'django.views.static.serve',{'document_root': RESOURCE_ROOT_PATH}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT_PATH}),
    url(r'^hotel$', 'hehotel.views.hotel', name='hotel'),
    #url(r'^rooms$', 'hehotel.views.rooms', name='rooms'),
    url(r'^rooms$', 'room.views_room_type.room_type_list', name='rooms'),
    url(r'^pictures$', 'hehotel.views.pictures', name='pictures'),
    url(r'^order$', 'hehotel.views.order', name='order'),
    url(r'^special_offers$', 'article.views.article_list', name='special_offers'),
    url(r'^member/', include('member.urls')),  # 用户模块
    url(r'^room/', include('room.urls')),  # 房间模块
    url(r'^order/', include('order.urls')),  # 订单模块
    url(r'^article/', include('article.urls')),  # 文章模块
    url(r'^sitemap$', 'hehotel.views.sitemap', name='sitemap'),
    url(r'^contactus$', 'hehotel.views.easy_page',{'template':'main/contactus.html'}, name='contactus'),
    url(r'^recruit$', 'hehotel.views.easy_page',{'template':'main/recruit.html'}, name='recruit'),
    url(r'^privacy$', 'hehotel.views.easy_page',{'template':'main/privacy.html'}, name='privacy'),
    #url(r'^privacy$', render_to_response,{'template_name':'mai/privacy.html'}, name='privacy'),
    
)
