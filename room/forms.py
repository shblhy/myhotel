#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from com.mylib import exforms
from room.models import Room,RoomType

class RoomForm(forms.ModelForm):
    room_type = forms.ModelChoiceField(RoomType)
    status = forms.IntegerField()
    photo = forms.CharField(label="photo",required=False)
    comment = forms.CharField(label="comment",required=False)
    note = forms.CharField(label="note",required=False)
    ref_id = forms.IntegerField(label="ref_id",initial=None,required=False)
    class Meta:
        model = Room


class RoomQForm(forms.Form):
    id = forms.CharField(label='id', required=False)#支持,分隔多项
    sn = forms.CharField(label='id', required=False)#支持,分隔多项
    name_like = forms.CharField(label='name_like', required=False)
    status = forms.CharField(label='status', required=False)
    using = forms.CharField(label='using', required=False)
    status_time = forms.CharField(label='status_time', required=False)
    iDisplayStart = exforms.PageField(default=0)
    iDisplayLength = exforms.PageField(default=30)
    orderBy = forms.CharField(label='', widget=forms.HiddenInput, required=False)
    
    def get_condition(self):
        form = self
        conditions = {}
        if form.cleaned_data.get('id',''):
            idIn = form.cleaned_data.get('id','').split(',')
            if idIn : conditions['id__in'] = idIn
        if form.cleaned_data.get('sn',''):
            snIn = form.cleaned_data.get('sn','').split(',')
            if snIn : conditions['sn__in'] = snIn
        if form.cleaned_data.get('name_like',''):
            conditions['name__contains'] = form.cleaned_data['name_like']
        if form.cleaned_data.get('status',''):
            conditions['status'] = form.cleaned_data['status'] 
        return conditions

class RoomTypeForm(forms.ModelForm):
    status = forms.IntegerField()
    photo = forms.CharField(label="photo",required=False)
    comment = forms.CharField(label="comment",required=False)
    note = forms.CharField(label="note",required=False)
    price = forms.IntegerField(required=True)
    class Meta:
        model = RoomType
        
    
    