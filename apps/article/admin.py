# -*- coding: utf-8 -*-
from django.contrib import admin
from libs.localdjex.admin import BaseListManager
from apps.article.models import Article


class ArticleListManager(BaseListManager):
    fields = ['id', 'title', 'content', 'author', 'edit_time', 'action']
    labels = {
              'action': u'操作'
              }
    accessors = {
                 'author': lambda x: x.author.real_name,
                 'action': BaseListManager.OUT_CALL
                 }
    model = Article

    @staticmethod
    def get_action(item, sign):
        actions = ['view']
        if sign:
            actions.append('edit')
            actions.append('delete')
        return ','.join(actions)

admin.site.register(Article)
