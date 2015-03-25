#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""



"""

from django import forms
from django.core.exceptions import ValidationError

class FieldRender(object):
    def __init__(self, field):
        self.id = field.id_for_label
        self.value = field.data
        self.label = field.label

    def render(self):
        return ''


class SelectRender(FieldRender):
    def render(self):
        return u'''
        $('#%s').prepend('<option%s></option>');
        $('#%s').select2({
            placeholder : "选择%s...",
            minimumResultsForSearch: 18,
            allowClear : true
        }); ''' % (self.id, ' selected' if self.value in [None, ''] else '', self.id, self.label)


class InputRender(FieldRender):
    pass


class FieldParam(object):
    def __init__(self, field):
        self.id = field.id_for_label
        self.name = field.name


class SelectParam(FieldParam):
    def param(self):
        return 'params["%s"] = $("#%s").select2("val");' % (self.name, self.id)



class InputParam(FieldParam):
    def param(self):
        return 'params["%s"] = $("#%s").val();' % (self.name, self.id)


class RenderFactory(object):
    render_dict = {
        'ModelChoiceField': SelectRender,
        'ChoiceField': SelectRender,
        'IPAddressField': InputRender,
        'CharField': InputRender,
    }

    param_dict = {
        'ModelChoiceField': SelectParam,
        'ChoiceField': SelectParam,
        'IPAddressField': InputParam,
        'CharField': InputParam,
    }

    @classmethod
    def init_render(cls, field):
        render_class = cls.render_dict.get(field.field.__class__.__name__)
        if render_class:
            return render_class(field)

    @classmethod
    def init_param(cls, field):
        param_class = cls.param_dict.get(field.field.__class__.__name__)
        if param_class:
            return param_class(field)


class ExForm(object):
    def populate_obj(self, obj):
        for name, value in self.cleaned_data.items():
            setattr(obj, name, value)
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

    def buttons(self):
        button_list = []
        for button in self.Meta.buttons:
            if not isinstance(button, Button):
                continue
            button_list.append(button.__json__())
        return button_list
    
    def get_conditions(self):
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


class PageField(forms.IntegerField):
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        if 'default' in kwargs:
            self.default = kwargs.pop('default')
        else:
            self.default = 0
        kwargs['widget'] = forms.HiddenInput
        kwargs['required'] = False
        kwargs['label'] = ''
        kwargs['min_value'] = 0
        super(PageField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(PageField, self).to_python(value)
        if value is None:
            value = self.default
        return value


class Button(object):
    '''<button type="button" class="btn">默认</button>'''
    type = 'button'
    _class = 'btn'
    name = ''
    def __init__(self, name, _class='btn', type='button'):
        self.name = name
        self._class = _class
        self.type = type

    def __json__(self):
        return '''<button type='%s' class='%s'>%s</button>
        ''' % (self.type, self._class, self.name)


class ReturnButton(Button):
    def __json__(self):
        return '''<a href="javascript:window.history.back()" class='%s'>%s</a>
        ''' % (self._class, self.name)


def validate_unique_caller(label, name, model_class, action, id=0):
    def caller(value):
        if action == 'new' and model_class.objects.filter(**{name: value}).exists():
            raise ValidationError(u'%s不能重复' % label)
        elif action == 'edit' and model_class.objects.exclude(id=id).filter(**{name: value}).exists():
            raise ValidationError(u'%s不能重复' % label)
    return caller


def validate_import_unique_caller(label, name, model_class):
    def caller(value):
        if model_class.objects.filter(**{name: value}).exists():
            raise ValidationError(u'%s不能重复' % label)
    return caller