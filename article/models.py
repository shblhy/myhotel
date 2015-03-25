# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from member.models import User

class Article(models.Model):
    title = models.CharField(_(u'标题'),max_length=64,blank=True)
    content = models.CharField(_(u'内容'),max_length=2000)
    author = models.ForeignKey(User,verbose_name=u'作者')
    insert_time = models.DateTimeField(_(u'插入时间'),auto_now_add=True)
    edit_time = models.DateTimeField(_(u'编辑时间'),auto_now_add=True)
    status =  models.IntegerField(_(u'状态'),default=0)
    #pictures =