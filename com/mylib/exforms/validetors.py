#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.core.exceptions import ValidationError


def validate_unique_caller(label, name, model_class, action, id=0):
    def caller(value):
        if action in ['new','add'] and model_class.objects.filter(**{name: value}).exists():
            raise ValidationError(u'%s不能重复' % label)
        elif action == 'edit' and model_class.objects.exclude(id=id).filter(**{name: value}).exists():
            raise ValidationError(u'%s不能重复' % label)
    return caller


def validate_import_unique_caller(label, name, model_class):
    def caller(value):
        if model_class.objects.filter(**{name: value}).exists():
            raise ValidationError(u'%s不能重复' % label)
    return caller
