#-*- coding:utf-8 -*-

from com.mylib.tables import tables
class OrderTable(tables.Table):
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