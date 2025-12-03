from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a7q*vtsm^)t0$qnillb8ey$0f8av%4q0l3^yl^d=u5vit*f1a='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'blog_db',
    'USER': 'root',
    'PASSWORD': '1234',
    'HOST': 'localhost',
    'PORT': '3306',
    }
}