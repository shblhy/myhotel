#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import time
import datetime
from decimal import Decimal

from django.utils.safestring import mark_safe

from com.mylib.tables.columns import Column
from com.mylib.tables.buttons import Button
from com.mylib.encoder import MyJSONEncoder
from sqlalchemy.util._collections import KeyedTuple

class Table(object):
    CALLBACK = 'reverse_accessors'
    
    """ Table

    Attributes:
        query: django query_set对象
        limit: 返回记录的最大行数
        offset: 起始记录行
        order_by: 排序，字符串，如：'-1,2,-3'表示第一列降序，第二列升序，第三列降序
        reverse_accessors: 反向数据访问器，用于导入数据时，作用相当于将select中的name转换为value
        validators: form表单额外的验证器，导入数据时用到
        pk_list: 保存查询结果记录的主键数据，用于跨数据库查询关联数据使用

    """

    def __init__(self, query, limit, offset=0, order_by='', reverse_accessors={}, validators={}):
        self.query = query
        self.limit = limit
        self.offset = offset
        self.order_by = order_by
        self.reverse_accessors = reverse_accessors
        self.validators = validators
        self.pk_list = None
        self.aaSorting = []
        self.unique_column = None

        self.columns = self.__class__._columns_()

    def parse_order_by(self):
        """解析排序字符串"""
        order_list = []
        for index in self.order_by.split(','):
            if not index: continue
            if index.startswith('-'):
                order_list.append('-' + self.columns[int(index[1:])].order_field)
                self.aaSorting.append([int(index[1:]), 'desc'])
            else:
                order_list.append(self.columns[int(index)].order_field)
                self.aaSorting.append([int(index), 'asc'])
        return order_list

    @classmethod
    def _columns_(cls):
        """Table的所有列，根据创建时间排序"""
        cols = []
        for name, column in cls.__dict__.items():
            if isinstance(column, Column):
                if column.field is None:
                    column.field = name
                if column.order_field is None:
                    column.order_field = column.field
                cols.append(column)
        cols.sort(lambda x, y: cmp(x.creation_counter, y.creation_counter))
        return cols
    
    def check_unique(self):
        for column in self.__class__._columns_():
            if column.unique:  # 循环table的所有columns时，设置table的唯一列，用于导入时字典的key
                self.unique_column = column.field
    
    def columns_exclude(self,excludes):
        excludesLabel = '_'.join([e for e in excludes])
        if not hasattr(self,'_columns_exclude_'+excludesLabel+'_'):
            res = []
            for c in self.columns:
                if not c.field in excludes:
                    res.append(c)
            setattr(self,'_columns_exclude_'+excludesLabel+'_',res)        
        return getattr(self,'_columns_exclude_'+excludesLabel+'_')
    
    @property
    def columns_exclude_action(self):
        return self.columns_exclude(['action'])
    
    def total(self):
        """总记录数"""
        return self.query.count()
    
    def rows(self, page=True,columns=None):
        if not columns:
            columns = self.columns
        q = self.query
        # 排序
        order_list = self.parse_order_by()
        if order_list: q = q.order_by(*order_list)
        # 分页
        if page:
            ret = q[self.offset:(self.offset+self.limit)]
            self.pk_list = [r.pk for r in ret]
        else:
            ret = self.query.all()

        rows = []
        for obj in ret:
            row = []
            for column in columns:
                if not page and not column.export: continue  # 如果是导出且该列不支持导出

                accessor = None  # 选择默认的数据访问器 
                if column.accessor == 'reverse_accessors':
                    accessor = self.reverse_accessors[column.field]
                elif page and column.accessor and callable(column.accessor):
                    accessor = column.accessor
                elif not page and column.export_accessor and callable(column.export_accessor):
                    accessor = column.export_accessor
                elif not page and column.accessor and callable(column.accessor):
                    accessor = column.accessor
                if accessor:
                    if accessor.func_code.co_argcount == 1:
                        r = accessor(obj)
                    else:
                        r = accessor(obj, self)
                else:
                    r = getattr(obj, column.field, '')

                if page:  # 字符串太长截取过长字符
                    v = getattr(obj, column.field, '')
                    if isinstance(v, basestring) and len(v) > column.truncate:
                        r = '<span title="%s">%s</span>' % (v, r.replace(v, v[:column.truncate]+'...'))
                row.append(r)
            rows.append(row)
        return rows

    def render(self, fmt):
        """view最后调用这个渲染方法返回所需要格式的数据"""
        if fmt == 'json':
            return {'total': self.total(), 'columns': self.columns, 'rows': self.rows()}
        elif fmt == 'csv':
            return {'columns': [column for column in self.columns if column.export], 'rows': self.rows(page=False)}

    def buttons(self):
        """将table meta中配置的buttons转化为前台需要字符串格式"""
        button_list = []
        for button in self.Meta.buttons:
            if not isinstance(button, Button):
                continue
            button_list.append('{\n' + ',\n'.join(button.__attrs__()) + '\n}')
        return '[' + ','.join(button_list) + ']'
    
    def get_columns(self,to_str=True):#适用于dataTable控件
        cols = [{'sTitle': c.sTitle, 'bSortable': c.bSortable, 'bVisible': c.bVisible} for c in self.columns]
        if to_str:
            return mark_safe(json.dumps(cols))
        else:
            return cols
    
    @classmethod
    def get_cls_columns(cls):
        return  mark_safe(json.dumps([{'sTitle': c.sTitle, 'bSortable': c.bSortable, 'bVisible': c.bVisible} for c in cls._columns_()]))
        
    def get_rows(self,to_str=True):#适用于dataTable控件
        result=[]
        for record in self.rows():
            #columns=table.columns|json total=table.total
            line = []
            for r in record:
                line.append(parse(r))
            result.append(line)
        res={
            "iTotalRecords": self.total(),
            "iTotalDisplayRecords": self.total(),
            "aaData": result
        }
        if to_str:
            return mark_safe(json.dumps(res,cls=MyJSONEncoder))
        else:
            return res
    class Meta():
        buttons = []
        checkbox = True


class TableAlchemy(object):
    """ TableAlchemy 用于SQLAlchemy ORM的表格插件

    Attributes:
        query: django query_set对象
        limit: 返回记录的最大行数
        offset: 起始记录行
        order_by: 排序，字符串，如：'-1,2,-3'表示第一列降序，第二列升序，第三列降序
        reverse_accessors: 反向数据访问器，用于导入数据时，作用相当于将select中的name转换为value
        validators: form表单额外的验证器，导入数据时用到
        sqlalchemy: True/False, Default:False, 是否是sqlalchemy查询，False为DjangoORM查询

    """

    def __init__(self, query, limit, offset=0, order_by='', reverse_accessors={}, validators={}):
        self.query = query
        self.limit = limit
        self.offset = offset
        self.order_by = order_by
        self.reverse_accessors = reverse_accessors
        self.validators = validators
        self.unique_column = None

        self.columns = self.__class__._columns_()
        self._rows = None

    def parse_order_by(self):
        """解析排序字符串,由于面对多表中相同参数的问题，与Table的parse_order_by方法有所不同"""
        order_list = []
        for index in self.order_by.split(','):
            if not index: continue
            if index.startswith('-'):
                inum = int(index[1:])
                order = ' desc'
            else:
                inum = int(index)
                order = ' asc'
            orderIndex = self.columns[inum].order_field
            if self.columns[inum].srctable and self.query:
                for col in self.query.column_descriptions:
                    if col['name'] == self.columns[inum].order_field and col['expr'].class_ == self.columns[inum].srctable:
                        break
                orderIndex = col['expr'].expression._label
            order_list.append(orderIndex + order)
            self.columns[int(index)].sSortingClass = 'sorting_asc'
        return order_list
    
    @classmethod
    def _columns_(cls):
        """Table的所有列，根据创建时间排序"""
        cols = []
        for name, column in cls.__dict__.items():
            if isinstance(column, Column):
                if column.field is None:
                    column.field = name
                if column.order_field is None:
                    column.order_field = column.field
                cols.append(column)
        cols.sort(lambda x, y: cmp(x.creation_counter, y.creation_counter))
        return cols
    
    def check_unique(self):
        for column in self.__class__._columns_():
            if column.unique:  # 循环table的所有columns时，设置table的唯一列，用于导入时字典的key
                self.unique_column = column.field
            
    def columns_exclude(self,excludes):
        excludesLabel = '_'.join([e for e in excludes])
        if not hasattr(self,'_columns_exclude_'+excludesLabel+'_'):
            res = []
            for c in self.columns:
                if not c.field in excludes:
                    res.append(c)
            setattr(self,'_columns_exclude_'+excludesLabel+'_',res)        
        return getattr(self,'_columns_exclude_'+excludesLabel+'_')
    
    @property
    def columns_exclude_action(self):
        return self.columns_exclude(['action'])
    
    def total(self):
        """总记录数"""
        if not hasattr(self,'_count_'):
            self._count_ = self.query.count()
        return self._count_

    def set_count(self,count):#为了加快速度，直接设置count
        self._count_ = count

    def rows(self, page=True,columns=None):
        if self._rows is not None:
            return self._rows
        else:
            q = self.query
            # 排序
            order_list = self.parse_order_by()
            if order_list: q = q.order_by(*order_list)
            # 分页
            if page:
                ret = q[self.offset:(self.offset+self.limit)]
            else:
                ret = self.query.all()
            rows = []
            for obj in ret:
                row = self.populate_obj(obj, page)
                rows.append(row)
            self._rows = rows
        return self._rows

    def render(self, fmt):
        """view最后调用这个渲染方法返回所需要格式的数据"""
        if fmt == 'json':
            return {'total': self.total(), 'columns': self.columns, 'rows': self.rows()}
        elif fmt == 'csv':
            return {'columns': [column for column in self.columns if column.export], 'rows': self.rows(page=False)}

    def populate_obj(self, obj, page=True):
        row = []
        for column in self.columns:
            if not page and not column.export: continue  # 如果是导出且该列不支持导出

            accessor = None  # 选择默认的数据访问器            
            if column.accessor == 'reverse_accessors':
                accessor = self.reverse_accessors[column.field]
            elif page and column.accessor and callable(column.accessor):
                accessor = column.accessor
            elif not page and column.export_accessor and callable(column.export_accessor):
                accessor = column.export_accessor
            elif not page and column.accessor and callable(column.accessor):
                accessor = column.accessor

            if accessor:
                if accessor.func_code.co_argcount == 1:
                    r = accessor(obj)
                else:
                    r = accessor(obj, self)
            else:
                r = getattr(obj, column.field, '')

            if page:  # 字符串太长截取过长字符
                v = getattr(obj, column.field, '')
                if isinstance(v, basestring) and len(v) > column.truncate:
                    r = '<span title="%s">%s</span>' % (v, r.replace(v, v[:column.truncate]+'...'))
            row.append(r)
        return row

    def buttons(self):
        """将table meta中配置的buttons转化为前台需要字符串格式"""
        button_list = []
        for button in self.Meta.buttons:
            if not isinstance(button, Button):
                continue
            button_list.append('{\n' + ',\n'.join(button.__attrs__()) + '\n}')
        return '[' + ','.join(button_list) + ']'

    def get_columns(self,to_str=True):#适用于dataTable控件
        cols = [{'sTitle': c.sTitle, 'bSortable': c.bSortable, 'bVisible': c.bVisible} for c in self.columns]
        if to_str:
            return mark_safe(json.dumps(cols))
        else:
            return cols

    @classmethod
    def get_cls_columns(cls):
        return  mark_safe(json.dumps([{'sTitle': c.sTitle, 'bSortable': c.bSortable, 'bVisible': c.bVisible} for c in cls._columns_()]))
    @staticmethod
    def aaaa():
        return 'aaaa'
    def get_rows(self,to_str=True):#适用于dataTable控件
        result=[]
        for record in self.rows():
            #columns=table.columns|json total=table.total
            line = []
            for r in record:
                line.append(parse(r))
            result.append(line)
        res={
            "iTotalRecords": self.total(),
            "iTotalDisplayRecords": self.total(),
            "aaData": result
        }
        if to_str:
            return mark_safe(json.dumps(res,cls=MyJSONEncoder))
        else :
            return res 
        
    class Meta():
        select_columns = []
        buttons = []
        checkbox = True

        
def parse(data):
    if isinstance(data, Decimal):
        data = float(data)
    elif isinstance(data, datetime.datetime):
        data = data.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(data, datetime.date):
        data = time.strftime("%Y/%m/%d", data.timetuple())
    elif isinstance(data, Column):
        data = data.__json__()
    return data
