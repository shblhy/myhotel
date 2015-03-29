# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from settings import RESOURCE_ROOT_PATH, STATIC_ROOT_PATH
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^templates/(?P<path>.*)$', 'django.views.static.serve', {'document_root': RESOURCE_ROOT_PATH}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT_PATH}),
    url(r'^admin/', 'hehotel.views.admin', name='admin'),  # 后台
    url(r'^backend/', include(admin.site.urls), name='backend'),  # 后台
    url(r'^backdocs/', include('django.contrib.admindocs.urls'), name='backdocs'),  # 后台
    url(r'^$', 'hehotel.views.index', name='index'),
    url(r'^hotel$', 'hehotel.views.hotel', name='hotel'),
    url(r'^pictures$', 'hehotel.views.pictures', name='pictures'),
    url(r'^order$', 'hehotel.views.order', name='order'),
    url(r'^rooms$', 'apps.room.views_room_type.room_type_list', name='rooms'),
    url(r'^special_offers$', 'apps.article.views.article_list', name='special_offers'),
    url(r'^member/', include('apps.member.urls')),  # 用户模块
    url(r'^room/', include('apps.room.urls')),  # 房间模块
    url(r'^order/', include('apps.order.urls')),  # 订单模块
    url(r'^article/', include('apps.article.urls')),  # 文章模块
    url(r'^site_map.html$', 'hehotel.views.sitemap', name='sitemap'),
    url(r'^contactus.html$', 'hehotel.views.easy_page', {'template': 'main/contactus.html'}, name='contactus'),
    url(r'^recruit.html$', 'hehotel.views.easy_page', {'template': 'main/recruit.html'}, name='recruit'),
    url(r'^privacy.html$', 'hehotel.views.easy_page', {'template': 'main/privacy.html'}, name='privacy'),
    url(r'^usage_clause.html$', 'hehotel.views.easy_page', {'template': 'main/usage_clause.html'}, name='privacy'),
    url(r'^map.html$', 'hehotel.views.easy_page', {'template': 'main/map.html'}, name='privacy')
)
