#-*- coding:utf-8 -*-
from django import forms
from apps.room.models import Room, RoomType
from libs.djex.forms import QForm, ModelForm, PageField


class RoomForm(ModelForm):
    room_type = forms.ModelChoiceField(RoomType)
    status = forms.IntegerField()
    photo = forms.CharField(label="photo", required=False)
    comment = forms.CharField(label="comment", required=False)
    note = forms.CharField(label="note", required=False)
    ref_id = forms.IntegerField(label="ref_id", initial=None, required=False)

    class Meta:
        model = Room
        exclude = ['status']


class RoomQForm(QForm):
    id = forms.CharField(label='id', required=False)
    sn = forms.CharField(label='id', required=False)
    name_like = forms.CharField(label='name_like', required=False)
    status = forms.CharField(label='status', required=False)
    #using = forms.CharField(label='using', required=False)
    #status_time = forms.CharField(label='status_time', required=False)
    iDisplayStart = PageField(label='记录起始点', default=0, required=False)
    iDisplayLength = PageField(label='记录长', default=30, required=False)
    orderBy = forms.CharField(label='', widget=forms.HiddenInput, required=False)

    def get_condition(self):
        form = self
        conditions = {}
        if form.cleaned_data.get('id', ''):
            idIn = form.cleaned_data.get('id', '').split(',')
            if idIn:
                conditions['id__in'] = idIn
        if form.cleaned_data.get('sn', ''):
            snIn = form.cleaned_data.get('sn', '').split(',')
            if snIn:
                conditions['sn__in'] = snIn
        if form.cleaned_data.get('name_like', ''):
            conditions['name__contains'] = form.cleaned_data['name_like']
        if form.cleaned_data.get('status', ''):
            conditions['status'] = form.cleaned_data['status']
        return conditions


class RoomTypeForm(ModelForm):
    class Meta:
        model = RoomType
        exclude = ['status']
