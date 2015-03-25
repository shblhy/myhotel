#!/usr/bin/env python
#-*- coding:utf-8 -*-


class Column(object):
    """ Table Column

    Attributes:
        sTitle: 列中文名称
        field: 字段名，如果为None，会默认使用列名
        accessor: 数据访问器，是一个回调方法，如果参数只有一个，这个参数为此条数据库记录,;如果有两个参数，另一个参数是table对象
        export: True或False，导出是否包含此列
        export_accessor: 导出时数据访问器，同accessor，因为导出时此列的格式可能跟页面时格式不一样，如果存在且用于导出，则会调用此访问器
        bSortable: True或False，该列是否支持排序
        creation_counter: 辅助属性，用于table创建列的顺序进行排序
        truncate: 截取字符串的长度，多余部分显示省略号
        unique: 是否唯一，用于导入时做主键
        bVisible: 默认是否显示
        order_field: 排序字段

    """
    creation_counter = 0

    def __init__(self, sTitle, field=None, accessor=None, export=True, export_accessor=None, bSortable=True,
                 truncate=20, unique=False, bVisible=True, order_field=None,srctable=None):
        self.sTitle = sTitle
        self.field = field
        self.accessor = accessor
        self.export = export
        self.export_accessor = export_accessor
        self.bSortable = bSortable
        self.truncate = truncate
        self.unique = unique
        self.bVisible = bVisible
        self.order_field = order_field
        self.srctable = srctable
        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1

    def __json__(self):
        return {'sTitle': self.sTitle, 'bSortable': self.bSortable, 'bVisible': self.bVisible}
