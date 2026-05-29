"""
Django settings for win_main project.
"""

from pathlib import Path
import os
from decouple import config

# --------------------------------------------------
# BASE DIR
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = 'django-insecure-*1nd_+n4_a+)zy^60xxj-l!9nkm*ha@w=o!fm*^9=_v&_qek9k'
DEBUG = True
ALLOWED_HOSTS = ['*']


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    'win_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'announcements',
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# --------------------------------------------------
# URLS & TEMPLATES
# --------------------------------------------------
ROOT_URLCONF = 'win_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'win_app.context_processors.menus',
                'win_app.context_processors.footer_sections',
                'win_app.context_processors.admission_status',
            ],
        },
    },
]

WSGI_APPLICATION = 'win_main.wsgi.application'


# --------------------------------------------------
# DATABASE (POSTGRESQL ✅)
# --------------------------------------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }



# --------------------------------------------------
# DATABASE (MYSQL)
# --------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'root',
        'PASSWORD': 'Shillong@itanagar',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
# DATABASE (MYSQL)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST', default='127.0.0.1'),
#         'PORT': config('DB_PORT', default='3306'),
#     }
# }

# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# STATIC & MEDIA
# --------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'win_main' / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# # --------------------------------------------------
# # EMAIL CONFIG (SAFE DEFAULTS ✅)
# # --------------------------------------------------
# EMAIL_HOST = config('EMAIL_HOST', default='localhost')
# EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')




# --------------------------------------------------
# EMAIL CONFIG (GMAIL SMTP)
# --------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'govindacharya51331@gmail.com'
EMAIL_HOST_PASSWORD = 'nszfhbfqntbusizg'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER