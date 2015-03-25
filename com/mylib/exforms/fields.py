#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe


class PageField(forms.IntegerField):
    #todo default 在 Field中提供了initial用以代替此功能，所以 根本不需要default。
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


class Tree(forms.TextInput):
    def __init__(self, attrs=None):
        super(Tree, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        return mark_safe(u'''
        <div class="select2-container %(class)s" id="%(id)s_select">
            <a tabindex="-1" class="select2-choice" onclick="return false;" href="javascript:void(0)">
                <span></span>
                <div> <b></b>
                </div>
            </a>
            <input type="hidden" id="%(id)s_input" name="%(name)s"></div>
        <div class="dropdown-menu">
            <div id="%(id)s_container" class="span3 well well-small">
                <div class="row-fluid medium-margin-bottom">
                    <a class="btn btn-primary span5">确定</a>
                    <a class="btn span5 offset1">取消</a>
                </div>
                <ul id="%(id)s" class="large-height overflow-y"></ul>
            </div>
        </div>
        ''' % {
            'id': attrs.get('id'),
            'name': name,
            'class': self.attrs.get('class'),
        })


class TreeField(forms.CharField):
    def __init__(self, default=[], url='', _class='pull-left small-width', *args, **kwargs):
        self.default = default
        self.url = url
        if not kwargs:
            kwargs = {}
        kwargs['widget'] = Tree(attrs={'class': _class})
        super(TreeField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if self.default and callable(self.default):
            self.default = self.default(value)
        return value


class CharDefaultField(forms.CharField):
    """支持默认值的CharField"""
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        if 'default' in kwargs:
            self.default = kwargs.pop('default')
        else:
            self.default = None
        super(CharDefaultField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(CharDefaultField, self).to_python(value).strip()
        if self.default is not None and not value:
            value = self.default
        return value


class MultiField(CharDefaultField):
    """ 多选Field，多个值是以逗号分隔的 """

    def to_python(self, value):
        value = super(MultiField, self).to_python(value)
        return value.split(',') if value else []


class MultiChoiceField(forms.MultipleChoiceField):
    """ 多选下拉Field，多个值是以逗号分隔的 """

    def to_python(self, value):
        if value:
            value = str(value).split(',')
        return super(MultiChoiceField, self).to_python(value)


class ModelMultiChoiceField(forms.ModelMultipleChoiceField):
    """ 多选ModelField，多个值是以逗号分隔的 """

    def to_python(self, value):
        value = str(value).strip().split(',')
        return super(MultiChoiceField, self).to_python(value)


class IntegerDefaultField(forms.IntegerField):
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        if 'default' in kwargs:
            self.default = kwargs.pop('default')
        else:
            self.default = 0
        super(IntegerDefaultField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(IntegerDefaultField, self).to_python(value)
        if value is None:
            value = self.default
        return value