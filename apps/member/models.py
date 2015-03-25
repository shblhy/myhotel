# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
        ])
    real_name = models.CharField(_('real name'), max_length=30, blank=True)
    #email = models.EmailField(_('email address'), blank=True,validators=EmailValidator)
    email = models.EmailField(_('email address'), blank=True)
    #qq =  models.CharField(_('qq'), max_length=30, blank=True,validators=QQValidator)
    qq = models.CharField(_('qq'), max_length=30, blank=True)
    #phone =models.CharField(_('phone'), max_length=30, blank=True,validators=PhoneValidator )
    phone = models.CharField(_('phone'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
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
