# -*- coding: utf-8 -*-
from django.contrib import admin
from libs.yhwork.admin import BaseListManager
from apps.room.models import Room, RoomType


class RoomListManager(BaseListManager):
    paginate_by = 100
    fields = ['id', 'sn', 'name', 'status', 'action']
    labels = {
              'action': u'操作'
              }
    exclude = []
    order_fields = ['store_id', 'province', 'store_name']
    accessors = {
                 'status': lambda x: x.get_status_display(),
                 'action': BaseListManager.OUT_CALL
                 }
    model = Room
    order_by = '-1'

    @staticmethod
    def get_action(item, user):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')
        return ','.join(actions)


class RoomTypeListManager(BaseListManager):
    paginate_by = 100
    fields = ['id', 'name', 'status', 'comment', 'price', 'action']
    labels = {'action': u'操作'}
    order_fields = ['id']
    accessors = {'action': BaseListManager.OUT_CALL}
    model = RoomType
    order_by = '-1'

    @classmethod
    def get_action(cls, room_type, user=None):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')
        actions.append('order')
        return ','.join(actions)

admin.site.register(Room)
admin.site.register(RoomType)
