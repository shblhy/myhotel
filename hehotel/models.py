# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Hotel(models.Model):
    '''保存酒店的详细信息以便查看'''
    name = models.CharField(_(u'名称'),max_length=64)
    contacts = models.CharField(_(u'联系电话'),max_length=64)
    member_id = models.CharField(_(u'会员ID'),max_length=32,null=True)
    article1 = models.CharField(_(u'文章1'),max_length=2000)
    article2 = models.CharField(_(u'文章2'),max_length=2000,)
    article3 = models.CharField(_(u'文章3'),max_length=2000)
    
    class Meta:
        db_table= 'hotel'
        
'''          
class File(models.Model):
    #附件存于static\file文件夹中,在数据库中保存其地址
    src = models.FileField(upload_to='auto',null=True)
    name = models.CharField(_(u'原始文件名'),max_length=255,null=True)
    note = models.CharField(_(u'备注'),max_length=255,null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=0,verbose_name='状态',help_text='1')
    
    class Meta:
        db_table= 'site_file'
'''