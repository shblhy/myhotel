# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Permission
from room.models import Room,RoomType
from room.forms import RoomQForm,RoomForm,RoomTypeForm
from libs.yhwork.admin import BaseListManager
from django.db.models import Count,Max
from datetime import datetime

class RoomListManager(BaseListManager):
    paginate_by = 100
    fields = ['id','sn','name','status','using','status_time','action'] #需要产生的域，例如表格头行数据
    labels = {
              'action':u'操作'
              } #在此获取label，如无则取model中已有定义的域label，再无则直接用域的名称。
    exclude = []
    search_fields = None #可用于搜索的域，也可以由search_form直接产生
    #search_form = None #关联到form
    order_fields = ['store_id','province','store_name'] #准许排序的域
    accessors = {
                 'action':BaseListManager.OUT_CALL
                 } #域取值办法，如lambda x: x.get_status_display() 其中x为该行model
    accessors_out = {} #域回调办法，当需要行
    model = Room
    search_form = RoomQForm
    #table_class = OurTable
    order_by = '-1'
    @staticmethod
    def get_action(item,user):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')
    
class RoomTypeListManager(BaseListManager):
    paginate_by = 100
    fields = ['id','name','status','comment','price','action'] #需要产生的域，例如表格头行数据
    labels = {
              'action':u'操作'
              } #在此获取label，如无则取model中已有定义的域label，再无则直接用域的名称。
    order_fields = ['id'] #准许排序的域
    accessors = {
                 'action':BaseListManager.OUT_CALL
                 } #域取值办法，如lambda x: x.get_status_display() 其中x为该行model
    model = RoomType
    order_by = '-1'
    
    @classmethod
    def get_action(cls,room_type,user=None):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')
        actions.append('order')
        return ','.join(actions)
    
admin.site.register(Room)
admin.site.register(RoomType)