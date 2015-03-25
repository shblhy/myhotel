# -*- coding: utf-8 -*-
from libs.yhwork.admin import BaseListManager
from apps.article.models import Article
from apps.article.forms import ArticleQForm


class ArticleListManager(BaseListManager):
    paginate_by = 100
    fields = ['id', 'title', 'content', 'author', 'edit_time', 'action']
    labels = {
              'action': u'操作'
              }
    exclude = []
    search_fields = None
    order_fields = ['id']
    accessors = {
                 'author': lambda x: x.author.real_name,
                 'action': BaseListManager.OUT_CALL
                 }
    accessors_out = {}
    model = Article
    search_form = ArticleQForm
    order_by = '-1'

    @staticmethod
    def get_action(item, user):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')
