#!/usr/bin/env python
#-*- coding:utf-8 -*-
#对应控件select2
class Select(object):
    control_name = 'select2'
    @staticmethod
    def to_page_text(d):
        return [{'value':key,'text':d[key],'selected':key in [0,1]} for key in d.keys()]
    