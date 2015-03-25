# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from member.models import User
from com.mylib.validators import SNVlaidator 

class RoomType(models.Model):
    name = models.CharField(_(u'房名'),max_length=200,unique=True)
    #photo = models.FileField(_(u'照片'),null=True)
    photo = models.CharField(_(u'照片'),max_length=200,null=True)
    comment = models.CharField(_(u'介绍'),max_length=2000)
    status = models.IntegerField(_(u'状态'),default=0)
    price = models.IntegerField(_(u'价格'),default=0)
    
    def full_photo_path(self):
        if self.photo:
            return '/static/upload/room_type/'+self.photo
        else:
            return ''
    
    def get_ready_room(self):
        return None
    
    class Meta:
        db_table = 'room_type'
        
        
class Room(models.Model):
    #sn = models.CharField(_(u'房号'),max_length=32,unique=True,validator=SNVlaidator)
    sn = models.CharField(_(u'房号'),max_length=32,unique=True)
    name = models.CharField(_(u'房名'),max_length=200,unique=True)
    photo = models.FileField(_(u'照片'),null=True)
    comment = models.CharField(_(u'介绍'),max_length=2000)
    RoomStatusChoices = {
                         -2:u'已删除',
                         -1:u'预备',
                         0:u'空闲',
                         1:u'预订',
                         2:u'在住',
                         }
    status = models.SmallIntegerField(_(u'状态'),choices= RoomStatusChoices.items(),default=0)
    '''RoomTypeChoices = {
                       0:u'单人房',
                       1:u'双人房',
                       2:u'贵宾房',
                       3:u'特惠房',
                       }
    rtype = models.SmallIntegerField(_(u'类别'),choices=RoomTypeChoices.items(),default=0)'''
    room_type = models.ForeignKey(RoomType)
    ref_id = models.IntegerField(_(u'关联'),null=True)#留着扩展，降低查询负担，暂不投入使用。
    note = models.CharField(_(u'备注'),max_length=2000,default='')

    class Meta:
        db_table = 'room'
        
class RoomHistory(models.Model):
    room_id = models.ForeignKey(Room)
    sn = models.CharField(_(u'房号'),max_length=32)
    photo = models.FileField(_(u'照片'))
    comment = models.CharField(_(u'介绍'),max_length=2000)
    RoomStatusChoices = {
                         -2:u'已删除',
                         -1:u'预备',
                         0:u'空闲',
                         1:u'预订',
                         2:u'在住',
                         }
    status = models.SmallIntegerField(_(u'状态'),choices=RoomStatusChoices.items(),default=0)
    RoomTypeChoices = {
                   0:u'单人房',
                   1:u'双人房',
                   2:u'贵宾房',
                   3:u'特惠房',
                   }
    rtype = models.SmallIntegerField(_(u'类别'),choices=RoomTypeChoices.items(),default=0)
    HistoryTypeChoices = {
                          0:'使用',
                          1:'编辑',
                          }
    type = models.SmallIntegerField(_(u'记录类别'),choices=HistoryTypeChoices.items(),default=0)
    ref_id = models.IntegerField(_(u'关联'),null=True)
    insert_time = models.DateTimeField(auto_now_add=True)
    opertor = models.ForeignKey(User)
    class Meta:
        db_table = 'room_history'
        