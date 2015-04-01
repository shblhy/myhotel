# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.room.models import Room, RoomType
from apps.member.models import User


class Order(models.Model):
    sn = models.CharField(_(u'订单号'), max_length=32, blank=True, null=True)
    customer = models.CharField(_(u'顾客姓名'), max_length=64, blank=True, null=True)
    phone = models.CharField(_(u'手机号'), max_length=64, blank=True, null=True)
    #member_id = models.CharField(max_length=32, null=True, verbose_name=u'用户ID，关联已注册用户')
    member = models.ForeignKey(User, verbose_name=u'顾客', null=True)
    note = models.CharField(_(u'备注'), max_length=2000, default='', blank=True)
    room_type = models.ForeignKey(RoomType, verbose_name=u'房型')
    room = models.ForeignKey(Room, null=True, blank=True)
    StatusChoices = {0: u'未支付', 1: u'已支付', 2: u'已使用'}
    status = models.SmallIntegerField(_(u'状态'), choices=StatusChoices.items(), default=0)
    use_time = models.DateTimeField(_(u'使用时间'), auto_now_add=True)
    use_days = models.SmallIntegerField(_(u'使用天数'), default=1)
    price = models.IntegerField(_(u'价格'), default=0)
    insert_time = models.DateTimeField(_(u'预订时间'), auto_now_add=True)

    def payed(self):
        return

    def set_creater(self, user):
        self.member_id = user.pk
        self.customer = user.real_name
        self.phone = user.phone
        return

    def set_sn(self):
        s = str(self.id)[:5]
        makeup = ''.join(['0'] * (6 - len(s)))
        self.sn = datetime.now().strftime('%y%m%d%H') + makeup + s
        self.save()
