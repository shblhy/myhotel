# -*- coding: utf-8 -*-
import random
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_(u'用户名'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
        ])
    real_name = models.CharField(_(u'实名'), max_length=30, blank=True)
    #email = models.EmailField(_('email address'), blank=True,validators=EmailValidator)
    email = models.EmailField(_('Email'), blank=True)
    #qq =  models.CharField(_('qq'), max_length=30, blank=True,validators=QQValidator)
    qq = models.CharField(_('QQ'), max_length=30, blank=True)
    #phone =models.CharField(_('phone'), max_length=30, blank=True,validators=PhoneValidator )
    phone = models.CharField(_(u'手机'), max_length=30, blank=True)
    is_staff = models.BooleanField(_(u'超级管理员'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_(u'活动的'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'

    def get_short_name(self):
        return self.username

    @staticmethod
    def easy_create_user(real_name, phone):
        def get_unique_username(name):
            for _i in range(0, 10):
                unique_name = name + '_' + str(random.randint(0, 10))
                if not User.objects.filter(username=unique_name).exists():
                    return unique_name
            raise Exception(u'无法自动生成用户名')
        username = get_unique_username(phone)
        datestr = datetime.now().strftime('%Y%m%d')
        password = datestr + phone[-4:]
        return User.objects.create_user(username, real_name=real_name, password=password, phone=phone), username, password
