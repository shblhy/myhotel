#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from libs.yhwork.forms import ModelForm, QForm, PageField
from apps.member.models import User
from apps.article.models import Article


class ArticleForm(ModelForm):
#    id = forms.CharField(label='id', required=False)#支持,分隔多项
#    username = forms.CharField(label='username', required=False)
#    real_name = forms.CharField(label='real_name', required=False)
#    qq = forms.CharField(label='',required = False)
#    phone = forms.CharField(label='',required = False)
    class Meta:
        model = Article
        exclude = ['status', 'author']


class ArticleQForm(QForm):
    #支持,分隔多项
    id = forms.CharField(label='id', required=False)
    title_like = forms.CharField(label='标题', required=False)
    author = forms.ModelChoiceField(User.objects, required=False)
    iDisplayStart = PageField(default=0, required=False)
    iDisplayLength = PageField(default=30, required=False)
    orderBy = forms.CharField(label='', widget=forms.HiddenInput, required=False)
