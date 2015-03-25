# -*- coding: utf-8 -*-
from django.contrib import admin
from libs.yhwork.admin import BaseListManager
from apps.order.models import Order


class OrderListManager(BaseListManager):
    paginate_by = 100
    fields = ['sn', 'status', 'use_time', 'room_type', 'use_days', 'note', 'price', 'action']
    labels = {
              'use_time': u'使用天数',# TODO 怪哉
              'action': u'操作'
              }
    exclude = []
    order_fields = ['id', 'room_type', 'status']
    accessors = {
                 'action': BaseListManager.OUT_CALL,
                 'status': lambda x: x.get_status_display(),
                 'room_type': lambda x: x.room_type.name
                 }
    accessors_out = {}
    model = Order
    order_by = '-1'

    @staticmethod
    def get_action(item, user):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')

admin.site.register(Order)
