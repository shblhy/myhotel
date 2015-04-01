#-*- coding:utf-8 -*-
from settings import *
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'hehotel',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'password',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3808'                    # Set to empty string for default. Not used with sqlite3.
        },
}

#是否在console窗口显示sql语句
SHOW_SQL = True
if SHOW_SQL:
    LOGGING['handlers']['console'] = {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
    }
    LOGGING['loggers']['django.db.backends'] = {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG',
            }

if SHOW_SQL:
    LOGGING['handlers']['console'] = {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
    }
    LOGGING['loggers']['django.db.backends'] = {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG',
            }
