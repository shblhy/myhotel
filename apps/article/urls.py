# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.article import views

urlpatterns = patterns('',
    url(r'^article_list$', views.article_list, name='article_articles'),
    url(r'^articles$', views.articles, name='admin_article_articles'),
    url(r'^articles.?(?P<contype>(page|table|csv))$', views.articles),
    url(r'^add$', views.article_input, name='admin_article_add'),
    url(r'^edit/(?P<article_id>[\d]+)$', views.article_input),
    url(r'^detail/(?P<article_id>[\d]+)$', views.article_detail),
    url(r'^input_article$', views.input_article, name='admin_article_add_action'),
    url(r'^edit_article$', views.input_article, name='admin_article_edit_action'),
    url(r'^delete_articles$', views.delete_articles),
)
