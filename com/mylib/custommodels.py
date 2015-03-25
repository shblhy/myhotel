#!/usr/bin/env python
from django.db.models.fields import (Field,SmallIntegerField,
                                     PositiveSmallIntegerField,
                                     AutoField,FloatField,IntegerField,CharField)
from django.db.models.fields import BooleanField as OriBooleanField
from com.mylib.models import Sequence
from django.core import exceptions, validators
from django.db import models
import re
class BooleanField(OriBooleanField):
    __metaclass__ = models.SubfieldBase
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "bit"
        else:
            return super(OriBooleanField, self).db_type(connection)
    def to_python(self, value):
        if value in (True, False):
            # if value is 1 or 0 than it's equal to True or False, but we want
            # to return a true bool for semantic reasons.
            return bool(value)
        if value in ('t', 'True', '1','\x01'):
            return True
        if value in ('f', 'False', '0','\x00'):
            return False
        msg = self.error_messages['invalid'] % str(value)
        raise exceptions.ValidationError(msg)
class SmallFloatField(FloatField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "float"
        else:
            return super(FloatField, self).db_type(connection)
class BlobField(Field):
    description = "Blob"
    def db_type(self, connection):
        return 'blob'
    
    
class TinyIntegerField(SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super(SmallIntegerField, self).db_type(connection)
        
        
class PositiveTinyIntegerField(PositiveSmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint unsigned"
        else:
            return super(PositiveTinyIntegerField, self).db_type(connection)
        
        
class PositiveSmallAutoField(AutoField):       
    def db_type(self,connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "smallint unsigned AUTO_INCREMENT"
        else:
            return super(AutoField, self).db_type(connection)
    def get_internal_type(self):
        return "PositiveSmallAutoField"
class PositiveTinyAutoField(AutoField):       
    def db_type(self,connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint unsigned AUTO_INCREMENT"
        else:
            return super(AutoField, self).db_type(connection)
    def get_internal_type(self):
        return "PositiveTinyAutoField"
class BigAutoField(AutoField):
    def db_type(self,connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "bigint AUTO_INCREMENT"
        else:
            return super(AutoField, self).db_type(connection)
    def get_internal_type(self):
        return "BigAutoField"
class SeqIntegerField(IntegerField):
    def pre_save(self, model_instance, add):
        if add :
            value = get_seq(1)
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(IntegerField, self).pre_save(model_instance, add)
class MyIPAddressField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 32 )
        kwargs['blank'] = True
        CharField.__init__(self, *args, **kwargs)
    #def pre_save(self, model_instance, add):
    #    ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
    #    validate_ipv4_address = RegexValidator(ipv4_re, _(u'Enter a valid IPv4 address.'), 'invalid')
        
def get_seq(i):
    try:
        maxItem = Sequence.objects.get(id=i)
        maxItem.seq=maxItem.seq+1
        maxItem.save()
    except:
        maxItem=Sequence()
        maxItem.seq=0
        maxItem.save()
    return maxItem.maxid