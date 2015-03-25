# -*- coding: utf-8 -*-
import re
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

class PhoneValidator(RegexValidator):
    regex = re.compile('^[0-9]{11}$')
    message = _(u'请输入11位手机号码。')
    
class QQValidator(RegexValidator):
    regex = re.compile('^[0-9]{3,14}$')
    message = _(u'请输入4-13位qq号码。')
    
class SNVlaidator(RegexValidator):
    regex = re.compile('^[-|_|0-9|a-z|A-Z|-]{2,10}$')
    message = _(u'请输入SN号，只能为字母数字及符号-_')