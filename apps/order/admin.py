# -*- coding: utf-8 -*-
import unittest
from django.contrib import admin
from libs.localdjex.admin import BaseListManager
from apps.order.models import Order


class OrderListManager(BaseListManager):
    fields = ['id', 'sn', 'status', 'customer', 'use_time', 'room_type', 'use_days', 'note', 'price', 'action']
    visible_fields = ['id']
    labels = {
              'customer': u'顾客姓名',
              'use_time': u'使用天数',
              'action': u'操作'
              }
    order_fields = ['id', 'sn', 'room_type', 'status']
    accessors = {
                 'action': BaseListManager.OUT_CALL,
                 'customer': lambda x: x.member.real_name if x.member else '',
                 'status': lambda x: x.get_status_display(),
                 'room_type': lambda x: x.room_type.name
                 }
    model = Order

    @staticmethod
    def get_action(item, user):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')
        return ','.join(actions)

admin.site.register(Order)


class OrderListManagerTest(unittest.TestCase):
    def runTest(self):
        self.test_roomtype_nomanysql()

    def test_roomtype_nomanysql(self):
        import django
        admin.site.unregister(Order)
        django.setup()
        condtions = {}
        q = Order.objects.filter(**condtions).select_related('room_type')
        for i in q:
            print i.room_type.name
        manager = OrderListManager(
             queryset=q,
             paginate_by=20,
             page=1,
             accessors_out={
                'action': lambda x: OrderListManager.get_action(x, None)
                }
        )
        print  manager.to_table().get_rows()
