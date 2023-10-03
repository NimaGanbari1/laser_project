import os
from pathlib import Path

#The local settings contains a series of information related to the project,
# which for some reason should not be distributed publicly, and this file does not exist in .gitignore file.
from . import local_settings


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = local_settings.SECRET

DEBUG = local_settings.DEB

ALLOWED_HOSTS = []

LOCAL_APPS = [
    'products',
    'users',
    'order', 
    'Authentication',
    'Cart',
    'AboutMe',
    
]

THIRD_PARTY_APPS = [
    'debug_toolbar',
    "django_mysql",
    'azbankgateways',
    "captcha",
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Application definition

INSTALLED_APPS = [
    *LOCAL_APPS,
    *DJANGO_APPS,
    *THIRD_PARTY_APPS
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'dj_laser.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dj_laser.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': local_settings.DB_NAME,
        'USER': local_settings.DB_USER,
        'PASSWORD': local_settings.DB_PASS,
        'HOST': local_settings.DB_HOST,
        'PORT': local_settings.DB_PORT,
        # Tell MySQLdb to connect with 'utf8mb4' character set
        "OPTIONS": {
            "charset": "utf8mb4",
        },
        # Tell Django to build the test database with the 'utf8mb4' character set
        "TEST": {
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'fa'
TIME_ZONE = 'UTC'
#TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Addressing for image storage
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

#To use personalized user
AUTH_USER_MODEL = 'users.user'


# cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
#This section is related to banking system settings

INTERNAL_IPS = [
   '127.0.0.1',
]


AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       'IDPAY': {
           'MERCHANT_CODE': local_settings.IDPAY_MERCHANT_CODE,
           'METHOD': 'POST',  # GET or POST
           'X_SANDBOX': 1,  # 0 disable, 1 active
       }
   },
   'IS_SAMPLE_FORM_ENABLE': True, # اختیاری و پیش فرض غیر فعال است
   'DEFAULT': 'IDPAY',
   'CURRENCY': 'IRR', # اختیاری
   'TRACKING_CODE_QUERY_PARAM': 'tc', # اختیاری
   'TRACKING_CODE_LENGTH': 16, # اختیاری
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader', # اختیاری
   'BANK_PRIORITIES': [
   ], # اختیاری
   'IS_SAFE_GET_GATEWAY_PAYMENT': False, #اختیاری، بهتر است True بزارید.
   'CUSTOM_APP': None, # اختیاری 
}


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    'allauth.account.auth_backends.AuthenticationBackend'
)

SITE_ID = 2

SOCIALACCOUNT_PROVIDERS = {
    "google":{
        "SCOPE":[
            "profile",
            "email"
        ],
        "AUTH_PARAMS":{"access_type":"online"}
    }
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'