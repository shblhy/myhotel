# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from apps.member.models import User
from libs.localdjex.admin import BaseListManager


class UserListManager(BaseListManager):
    fields = ['id', 'username', 'real_name', 'phone', 'email', 'qq', 'action']
    labels = {
              'action': u'操作'
              }
    accessors = {
                 'action': BaseListManager.OUT_CALL
                 }
    accessors_out = {}
    model = User

    @classmethod
    def get_action(cls, room, user=None):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        return ','.join(actions)


class GroupListManager(BaseListManager):
    paginate_by = 100
    fields = ['id', 'name', 'action']
    labels = {
              'action': u'操作'
              }
    exclude = []
    search_fields = None
    order_fields = ['id']
    accessors = {
                 'action': BaseListManager.OUT_CALL
                 }
    accessors_out = {}
    model = Group
    order_by = '-1'

    @classmethod
    def get_action(cls, room, user=None):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        return ','.join(actions)

admin.site.register(User)
