#!/usr/bin/env python
#-*- coding:utf-8 -*-


class Button(object):
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
