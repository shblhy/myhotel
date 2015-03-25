#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
#from com.mylib import exforms
from libs.yhwork.forms import Form,ModelForm,QForm,PageField
from member.models import User

class UserForm(ModelForm):
#    id = forms.CharField(label='id', required=False)#支持,分隔多项
#    username = forms.CharField(label='username', required=False)
#    real_name = forms.CharField(label='real_name', required=False)
#    qq = forms.CharField(label='',required = False)
#    phone = forms.CharField(label='',required = False)
    class Meta:
        model = User
        exclude = ['is_staff','is_active','date_joined','last_login']
    
class UserQForm(QForm):
    id = forms.CharField(label='id', required=False)#支持,分隔多项
    username = forms.CharField(label='username', required=False)
    real_name = forms.CharField(label='real_name', required=False)
    qq = forms.CharField(label='',required = False)
    phone = forms.CharField(label='',required = False)
    iDisplayStart = PageField(default=0)
    iDisplayLength = PageField(default=30)
    orderBy = forms.CharField(label='', widget=forms.HiddenInput, required=False)
    