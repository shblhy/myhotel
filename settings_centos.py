#-*- coding:utf-8 -*-
"""
Django settings for hehotel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6@j!6%foulnrume$wc7i5cwc2ppf6hcxoa&xh_vtanfy_rc@yc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
EXCEPTION_INGORE_AJAX = True #异常信息即便是ajax请求也直接返回Html页面

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
RESOURCE_ROOT_PATH = os.path.join(BASE_DIR, 'templates').replace('\\','/')
#STATIC_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates\static').replace('\\','/')
STATIC_ROOT_PATH = os.path.join(BASE_DIR, 'static').replace('\\','/')

ALLOWED_HOSTS = []


# Application definition
SITE_ID = 1

AUTH_USER_MODEL = 'member.User'

INSTALLED_APPS = (
    'apps.member',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'hehotel',
    'apps.room',
    'apps.order',
    'apps.article',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'hehotel',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD':'9729e316fb01',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '36114'                    # Set to empty string for default. Not used with sqlite3.
        },
    #'easy':{
    #   'ENGINE': 'django.db.backends.sqlite3',
    #  'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #},
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh_CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/__static__/'

SHOW_SQL = True#是否在console窗口显示sql语句
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
             'level': 'INFO',
             'class': 'logging.FileHandler',
             #'formatter': 'simple',
             'filename': os.path.join(os.path.dirname(__file__), 'logs/auto.log'),
             'mode': 'a',
         }
    },
    'loggers': {
        'log':{
           'handlers': ['file'],
           #'filters': ['special'],
           'level': 'INFO',
           'propagate': True
        }  
    }
}
if SHOW_SQL:
    LOGGING['handlers']['console']={
        'level':'DEBUG',
        'class':'logging.StreamHandler',
    }
    LOGGING['loggers']['django.db.backends']= {
                'handlers': ['console'],
                'propagate': True,
                'level':'DEBUG',
            }
