#-*- coding:utf-8 -*-

from com.mylib.tables import tables


class UserTable(tables.Table):
    id = tables.Column(sTitle=u'ID',bSortable=False)
    username = tables.Column(sTitle=u'用户名', bSortable=False)
    real_name = tables.Column(sTitle=u'姓名', bSortable=False)
    phone = tables.Column(sTitle=u'状态时间', bSortable=False)
    email = tables.Column(sTitle=u'状态', bSortable=False)
    qq = tables.Column(sTitle=u'使用者', bSortable=False)    
    action= tables.Column(sTitle=u'操作', bSortable=False, accessor=tables.Table.CALLBACK)
    
    @classmethod
    def get_action(cls,room,user=None):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        return ','.join(actions)
    
class GroupTable(tables.Table):
    id = tables.Column(sTitle=u'ID',bSortable=False)
    name = tables.Column(sTitle=u'名称', bSortable=False)
    action= tables.Column(sTitle=u'操作', bSortable=False, accessor=tables.Table.CALLBACK)
    
    @classmethod
    def get_action(cls,room,user=None):
        actions = ['view']
        actions.append('edit')
        actions.append('delete')
        return ','.join(actions)