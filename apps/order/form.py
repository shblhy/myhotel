#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from libs.yhwork.forms import ModelForm, QForm, PageField
from apps.order.models import Order
from apps.room.models import Room, RoomType
from apps.member.models import User


class OrderForm(ModelForm):
    member = forms.ModelChoiceField(User.objects, required=False)

    class Meta:
        model = Order
        exclude = ['status', 'insert_time', 'price']


class OrderQForm(QForm):
    sn = forms.CharField(label=u'订单号', required=False)
    customer = forms.CharField(label=u'顾客', required=False)
    phone = forms.CharField(label=u'手机号', required=False)
    member = forms.ModelChoiceField(User.objects, required=False)
    note = forms.CharField(label=u'备注', required=False)
    room_type = forms.ModelChoiceField(RoomType.objects, required=False)
    room = forms.ModelChoiceField(Room.objects, required=False)
    status = forms.IntegerField(label=u'状态', required=False)
    note_like = forms.CharField(label=u'备注', required=False)
    iDisplayStart = PageField(default=0, required=False)
    iDisplayLength = PageField(default=30, required=False)
    orderBy = forms.CharField(label='', widget=forms.HiddenInput, required=False)

    def get_condition(self):
        return QForm.get_conditions(self)
