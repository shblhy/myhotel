# -*- coding: utf-8 -*-
#!/usr/bin/env python

from datetime import datetime
from django.db.models.base import ModelBase

class HandlerFactory(object):
    """
    Handler工厂，提供统一的方法生产所需的Handler
    """

    @classmethod
    def get_handler(self, handler_name):
        """
        根据handler_name, 获取Handler

        Args:
            handler_name: Handler名称，初步设计为全路径名(包名.模块名.Handler类名),如：'appear.handlers.TestHandler'

        Returns:
            Handler类
        """
        path = handler_name.split('.')
        module = __import__('.'.join(path[:-1]), fromlist=[path[-2]])
        if hasattr(module, path[-1]):
            return getattr(module, path[-1])
        else:
            raise Exception(u'Handler的全路径名称有误')


class HandlerBase(object):
    """
    所有Handler类都应该继承此类
    """

    def __init__(self, request, **kwargs):
        """
                        从Request对象中获取参数传递给所有的Field
        Args:
            request: Http Request对象
            kwargs: 用于在request以外获取字段值
        """
        self.request = request
        self.fields = []
        self._init_field(request, **kwargs)

    def _init_field(self, request, **kwargs):
        for name, field in self.__class__.__dict__.items():
            if not isinstance(field, HandlerField):
                continue

            if field.name is None:  # 如果字段没有指定name, 默认采用变量名
                field.name = name

            if field.name in kwargs:  # 如果kwargs传了值，将不会在request中获取
                field.value = kwargs[field.name]
            else:
                if field.req_getlist:  # 如果request获取的参数是列表
                    value_list = []
                    for value in getattr(request, request.method).getlist(field.name, field.default):
                        if value == '': continue
                        if field.field_type == 'datetime' and value and type(value) != datetime:
                            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        elif field.field_type == 'int' and value and type(value) != int:
                            value = int(value)
                        value_list.append(value)
                    field.value = value_list
                else:
                    value = getattr(request, request.method).get(field.name, field.default)
                    if field.field_type == 'datetime' and value and type(value) != datetime:
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    elif field.field_type == 'int' and value and type(value) != int:
                        value = int(value)
                    field.value = value

            if field.value and type(field.field_type) == ModelBase:  # 如果field_type是DjangoModel
                if field.req_getlist:
                    field.value = field.field_type.objects.filter(pk__in=field.value)
                else:
                    field.value = field.field_type.objects.get(pk=field.value)

            self.fields.append(field)

    def query(self):
        """根据参数查询结果"""
        pass

    def output(self, output_type):
        """ 根据输出类型获取结果。 如果output_type='table',实际上是调用output_table方法。"""
        if hasattr(self, 'output_'+str(output_type)) and callable(getattr(self, 'output_'+str(output_type))):
            return getattr(self, 'output_'+str(output_type))()
        else:
            raise Exception(u'不支持的输出类型')

    def output_table(self):
        """输出为表格table"""
        pass


class HandlerField(object):
    """
    Handler类字段的基类
    """

    def __init__(self, verbose_name=None, name=None, default=None, req_getlist=False, field_type='str'):
        """
        Args:
            verbose_name: 中文名称
            name: 英文名称
            default: 默认值
            req_getlist: 确定从Request获取value的时候是否采用getlist方法，默认为False，不使用
            type: 类型
        """
        self.verbose_name = verbose_name
        self.name = name
        self.default = default
        self.req_getlist = req_getlist
        self.field_type = field_type
        self.value = None


# 测试
if __name__ == "__main__":

    handler = HandlerFactory.get_handler('appear.handlers.OverallHandler')

    handler().output_table()