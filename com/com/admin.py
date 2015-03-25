# -*- coding: utf-8 -*-
'''
内容管理，实现内容到json的转换以适应前端控件要求。
'''
from django.views.generic.list import MultipleObjectMixin
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.forms.models import fields_for_model
from django.db.models import AutoField
from wiwidebd.libs.com.widget import Table,Select
from django.utils.translation import ugettext_lazy as _

class OutManager(object):
    """
    目标：将数据转变为json等常规格式，以提供给前端处理。
    原计划模拟View编写，可同时处理django orm与sqlalchemy等多种格式数据，但考虑到开发难度目前只支持Model。
    from django.views.generic.base import View
    """
    fields = [] #需要产生的域，例如表格头行数据
    visible_fields = [] #不可见的域
    search_fields = None #可用于搜索的域，也可以由search_form直接产生
    order_fields = [] #准许排序的域
    accessors = {} #域取值办法，如'attr1':lambda x: x.get_status_display() 其中x为该行model
    accessors_out = {} #域回调办法，当需要外部参数传入时使用
    labels = {} #域名称，如果此处未定义则取model内容
    #kwargs = {}
    paginator_class = Paginator
    table_class = Table
    select_class = Select
    _data_cache = None
    OUT_CALL = 'accessors_out'
    
#ListView
class BaseListManager(MultipleObjectMixin,OutManager):
    
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def paginate_queryset(self, queryset, page_size):
        """
        分页
        """
        paginator = self.get_paginator(queryset, page_size, allow_empty_first_page=self.get_allow_empty())
        try:
            page_number = int(self.page)
        except ValueError:
            if self.page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(u"参数page无法转化为正确页码"))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage:
            raise Http404(_(u'无效页码(%(page_number)s)') % {
                                'page_number': page_number
            })

    @property
    def data(self):
        if self._data_cache is None:
            self._data_cache = self.get_context_data(object_list=self.get_queryset())
        return self._data_cache 
    
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
    
    def get_line(self,item,excludes=[]):
        '''
        将对象转变为行输出
        '''
        line = []
        for field in self.fields+self.visible_fields:
            if field in excludes:
                continue
            func = self.accessors.get(field,None)
            if  func == OutManager.OUT_CALL: func = self.accessors_out[field]
            attr = func(item) if func else getattr(item,field) if type(item) <> dict else item.get('field','')
            line.append(attr)
        return line
        
    def get_rows_data(self):
        return [self.get_line(item) for item in self.data['object_list']]
    
    @property
    def objs(self):
        return self.data['object_list']
    
    def to_table(self,**kwargs):
        table_args = {
                      'rows':self.get_rows_data(),
                      'columns':self.get_field_labels(),
                      'visible_columns':[(v,'') for v in self.visible_fields],
                      'page_size':self.paginate_by,
                      'page':self.page,
                      'total':self.data['paginator'].count,
                      'num_pages':self.data['paginator'].num_pages,
                      }
        table_args.update(kwargs)
        return self.table_class(**table_args)
    
    def get_field_labels(self):
        '''
            返还域数组，形如[(field,label),]
        '''
        return [(field,type(self).field_label(field))  for field in self.fields]
    
    @classmethod
    def field_label(cls,field):
        if not hasattr(cls,'base_fields'):
            '''
            def tran_form_field(field,**kwargs):
                if type(field)==AutoField:
                    defaults = {'form_class': IntegerField}
                    defaults.update(kwargs)
                    return IntegerField.formfield(field,**defaults)
                else:
                    return field.formfield(field,**kwargs)
                #f = lambda x:IntegerField.formfield(x) if type(x)==AutoField else x.formfield()
            '''
            cls.base_fields = fields_for_model(cls.model,cls.fields,cls.exclude,None,None)
            '''AutoField djangoform并未为其产生formfield'''
            for f in cls.model._meta.fields:
                if type(f) == AutoField:
                    f.label = f.verbose_name
                    cls.base_fields[f.name] = f
        return cls.labels[field] if cls.labels.has_key(field) else (unicode(cls.base_fields[field].label if (cls.base_fields.has_key(field) and cls.base_fields[field] is not None) else field))
    
    def to_chart(self):
        pass
    
    def to_select(self):
        return