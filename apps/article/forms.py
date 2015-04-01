#-*- coding:utf-8 -*-

from django import forms
from libs.djex.forms import ModelForm, QForm, PageField
from apps.member.models import User
from apps.article.models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['status', 'author']


class ArticleQForm(QForm):
    #支持,分隔多项
    id = forms.CharField(label='id', required=False)
    title_like = forms.CharField(label='标题', required=False)
    author = forms.ModelChoiceField(User.objects, required=False)
    iDisplayStart = PageField(label='记录起始点', default=0, required=False)
    iDisplayLength = PageField(label='记录长', default=30, required=False)
    orderBy = forms.CharField(label='', widget=forms.HiddenInput, required=False)
