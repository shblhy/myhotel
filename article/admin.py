# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Permission
from article.models import Article
from article.forms import ArticleQForm
from libs.yhwork.admin import BaseListManager


class ArticleListManager(BaseListManager):
    paginate_by = 100
    fields = ['id', 'title', 'content', 'author', 'edit_time', 'action'] #需要产生的域，例如表格头行数据
    labels = {
              'action': u'操作'
              }
    #在此获取label，如无则取model中已有定义的域label，再无则直接用域的名称。
    exclude = []
    search_fields = None
    #可用于搜索的域，也可以由search_form直接产生
    #search_form = None #关联到form
    #准许排序的域
    order_fields = ['id']
    accessors = {
                 'author': lambda x:x.author.real_name,
                 'action': BaseListManager.OUT_CALL
                 }
    accessors_out = {}
    model = Article
    search_form = ArticleQForm
    #table_class = OurTable
    order_by = '-1'
    @staticmethod
    def get_action(item,user):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')