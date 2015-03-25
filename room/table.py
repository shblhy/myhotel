#-*- coding:utf-8 -*-

from com.mylib.tables import tables
class RoomTypeTable(tables.Table):
    id = tables.Column(sTitle=u'ID',bSortable=False)
    name = tables.Column(sTitle=u'名称', bSortable=False)
    status = tables.Column(sTitle=u'状态', bSortable=False)
    comment = tables.Column(sTitle=u'说明', bSortable=False)
    price = tables.Column(sTitle=u'价格', bSortable=False)
    action= tables.Column(sTitle=u'操作', bSortable=False, accessor=tables.Table.CALLBACK)    
    
    @classmethod
    def get_action(cls,room_type,user=None):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')
        actions.append('order')
        return ','.join(actions)


class RoomTable(tables.Table):
    id = tables.Column(sTitle=u'ID',bSortable=False)
    sn = tables.Column(sTitle=u'房号', bSortable=False)
    name = tables.Column(sTitle=u'名称', bSortable=False)
    status = tables.Column(sTitle=u'状态', bSortable=False, accessor=lambda x: x.get_status_display())
    using = tables.Column(sTitle=u'使用者', bSortable=False, accessor=lambda x: x.order_set.all()[0].customer if x.status in [] else  u'无')
    status_time = tables.Column(sTitle=u'状态时间', bSortable=False, accessor=lambda x:'')
    action= tables.Column(sTitle=u'操作', bSortable=False, accessor=tables.Table.CALLBACK)
    
    @classmethod
    def get_action(cls,room,user=None):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        actions.append('add')
        
        '''
        if user.hasperm('room.edit_room'):
            actions.append('edit') 
        if user.hasperm('room.delete_room'):
            actions.append('delete') 
        if user.hasperm('room.add_room'):
            actions.append('add')
        '''
        return ','.join(actions)
        