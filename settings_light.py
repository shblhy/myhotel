#-*- coding:utf-8 -*-
from settings import *
DEBUG = True
DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
      'NAME': os.path.join(os.path.join(BASE_DIR, 'data'), 'db.sqlite3'),
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
