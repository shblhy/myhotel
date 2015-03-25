# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^article_list$','article.views.article_list',name='article_articles'),
    url(r'^articles$','article.views.articles',name='admin_article_articles'),
    url(r'^articles.?(?P<contype>(page|table|csv))$', 'article.views.articles'),
    #url(r'^articles.?(?P<contype>(page|table|csv))$', 'article.views.articles',name="admin_article_articles_table"),
    url(r'^add$','article.views.article_input',name='admin_article_add'),
    url(r'^edit/(?P<article_id>[\d]+)$','article.views.article_input',{'action':'edit'}),
    url(r'^detail/(?P<article_id>[\d]+)$','article.views.article_detail'),
    
    url(r'^input_article$','article.views.input_article',name='admin_article_add_action'),
    url(r'^edit_article$','article.views.input_article',{'action':'edit'},name='admin_article_edit_action'),
    url(r'^delete_articles$','article.views.delete_articles'),
)