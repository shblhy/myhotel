#-*- coding:utf-8 -*-
from django import forms
from libs.djex.forms import ModelForm, QForm, PageField
from apps.member.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'date_joined', 'last_login']


class UserQForm(QForm):
    id = forms.CharField(label='id', required=False)#支持,分隔多项
    username = forms.CharField(label='username', required=False)
    real_name = forms.CharField(label='real_name', required=False)
    qq = forms.CharField(label='', required=False)
    phone = forms.CharField(label='', required=False)
    iDisplayStart = PageField(label='记录起始点', default=0, required=False)
    iDisplayLength = PageField(label='记录长', default=30, required=False)
    orderBy = forms.CharField(label='', widget=forms.HiddenInput, required=False)
