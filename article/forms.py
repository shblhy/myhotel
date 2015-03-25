#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from libs.yhwork.forms import ModelForm,QForm,PageField
from member.models import User
from article.models import Article

class ArticleForm(ModelForm):
#    id = forms.CharField(label='id', required=False)#支持,分隔多项
#    username = forms.CharField(label='username', required=False)
#    real_name = forms.CharField(label='real_name', required=False)
#    qq = forms.CharField(label='',required = False)
#    phone = forms.CharField(label='',required = False)
    class Meta:
        model = Article
        exclude = ['status','author']
    
class ArticleQForm(QForm):
    id = forms.CharField(label='id', required=False)#支持,分隔多项
    username = forms.CharField(label='username', required=False)
    real_name = forms.CharField(label='real_name', required=False)
    qq = forms.CharField(label='',required = False)
    phone = forms.CharField(label='',required = False)
    page = PageField(default=0)
    page_size = PageField(default=30)
    orderBy = forms.CharField(label='', widget=forms.HiddenInput, required=False)
    