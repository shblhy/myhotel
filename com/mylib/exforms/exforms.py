#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""



"""

from com.mylib.exforms.renders import RenderFactory
from com.mylib.exforms.buttons import Button


class ExForm(object):
    def populate_obj(self, obj):
        for name, value in self.cleaned_data.items():
            setattr(obj, name, value.strip() if isinstance(value, basestring) else value)
        return obj

    def render_js(self):
        if self.Meta.include_render is None:
            renders = [RenderFactory.init_render(field) for field in self if not field.is_hidden]
        else:
            renders = []
            for item in self.Meta.include_render:
                if isinstance(item, basestring):
                    if item in self.Meta.exclude_render: continue
                    if not hasattr(self, item): continue
                    renders.append(RenderFactory.init_render(getattr(self, item)))
                else:
                    renders.append(item)
        result = []
        for render in renders:
            if render:
                result.append(render.render())
        return result

    def param_js(self):
        if self.Meta.include_param is None:
            params = [RenderFactory.init_param(field) for field in self if not field.is_hidden]
        else:
            params = []
            for item in self.Meta.include_param:
                if isinstance(item, basestring):
                    if item in self.Meta.exclude_param: continue
                    if not hasattr(self, item): continue
                    params.append(RenderFactory.init_param(getattr(self, item)))
                else:
                    params.append(item)
        result = [
            'var get_params = function() {',
            'var params = {};'
        ]
        for param in params:
            if param:
                result.append(param.param())
        result.append('return params;')
        result.append('}')
        return result
    
    def get_errmsg(self):
        return self.base_fields[self.errors.keys()[0]].label+':'+self.errors[self.errors.keys()[0]][0]
    
    def buttons(self):
        button_list = []
        for button in self.Meta.buttons:
            if not isinstance(button, Button):
                continue
            button_list.append(button.__json__())
        return button_list
    
    def get_condition(self):
        '''遍历form所有字段，如果cleaned_data存在它，则它作为数据库查询条件'''
        conditions = {}
        for key in self.cleaned_data:            
            if not key in ['iDisplayLength','iDisplayStart','orderBy'] and self.cleaned_data.get(key):
                conditions[key] = self.cleaned_data[key]
        return conditions
    
    class Meta():
        buttons = []
        include_render = None
        exclude_render = []
        include_param = None
        exclude_param = []