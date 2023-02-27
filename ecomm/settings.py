"""
Django settings for ecomm project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from ecomm.vendors import data

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--d&7$r=0hy@(e6_wbix9b!5bqhmsw6hzka-@t@3%e&&^o6&2o-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'ecomm.apps.account.apps.AccountConfig',
    'ecomm.apps.company.apps.CompanyConfig',
    'ecomm.apps.shop.apps.ShopConfig',
    'ecomm.apps.category.apps.CategoryConfig',
    'ecomm.apps.product.apps.ProductConfig',
    'ecomm.apps.delivery.apps.DeliveryConfig',
    'ecomm.apps.brand.apps.BrandConfig',
    'ecomm.apps.sale.apps.SaleConfig',
    'ecomm.apps.stock.apps.StockConfig',
    # extensions
    'mptt',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecomm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ecomm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dj_ecomm_app_db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = data.LIST_OF_LANGUAGES
LANGUAGE_CODES = data.LIST_OF_LANGUAGE_CODES

LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static and media files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'ecomm/apps/company/static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CUSTOM USER
AUTH_USER_MODEL = 'account.Account'

# DEFAULT 
NUMBER_PER_PAGE = 15
NUMBER_PAGINATIONS = 10

MIN_PRICE = 0.01
MAX_PRICE = 1_000_000
MIN_DELIVERY_PRICE = 0.00

IMAGE_WIDTH = {
    'THUMBNAIL': 60,
    'SHOWCASE': 220,
    'SLIDER': 500,
    'LOGO': 170,
}

COMPANY_ALIAS = 'grkr'
EMPTY_VALUE = '_'

# REDIRECT_TO_IF_AUTHENTICATED = '/'

# LOGIN_REDIRECT_URL = '/account/dashboard/'
# LOGIN_URL = '/account/signin/'

DEFAULT_IMAGE = {
    'PLACEHOLDER': 'company/images/default/placeholder.png',
    'LOGO':        'company/images/default/logo.png',
    'ICON':        'company/images/default/icon.png',
}
DEFAULT_IMAGE_KEY = list(DEFAULT_IMAGE)[0]

CACHE_TIMEOUT = {
    'YEAR':         60 * 60 * 24 * 364,
    'MONTH':        60 * 60 * 24 * 364,
    'DAY':          60 * 60 * 24 * 364,
    'FIVE_MINUTES': 60 * 60 * 5
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'cache',
    }
}

AUTHENTICATION_BACKENDS = [
    'ecomm.vendors.utils.auth.AccountBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# SMTP
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 465 #587
# #EMAIL_USE_TLS = True # EMAIL_USE_SSL = True
# EMAIL_HOST_USER = '??????@gmail.com'
# EMAIL_HOST_PASWORD = '***********'

# LOGGING
LOG_PATH = BASE_DIR / 'log/'
LOG_MAX_BYTES = 1024 * 1024 * 10 # 10Mb
LOG_BACKUP_COUNT = 10

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime}:{levelname}:{module}:{filename}:{lineno}:{message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file_rotating': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH / 'main.log',
            'maxBytes': LOG_MAX_BYTES, 
            'backupCount': LOG_BACKUP_COUNT,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['file_rotating', 'console'],
            'level': 'DEBUG',
        },
    },
}

# CELERY
REDIS_HOST = '0.0.0.0'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://'+REDIS_HOST+':'+REDIS_PORT+'/0'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'redis://'+REDIS_HOST+':'+REDIS_PORT+'/0'


# PAYPAL
CLIENT_ID = 'ARq8zA5Dbrdn3elQrn5k97H-NIDJSsDvLzHrqli1e0H2t0vLGyioRm2qwi1K0XGfAo-4_MfsbpeyfLzK'
CLIENT_SECRET = 'EDd7Saj1aKGruvefK38zhqlssB-0IOad9j5lFs9nuaMxNH2n3HJmHGxFuwH74L3Xd0eGxfD_10b7Wtpm'
test_pay_email = 'sb-4m5jo20987729@personal.example.com'
test_pay_password ='3yH5.L7>'

HIDDEN_SVG = '<svg \
xmlns="http://www.w3.org/2000/svg" \
width="40" height="40" fill="currentColor" viewBox="0 0 16 16">\
<path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 \
0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.\
48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486l.708.709z"/><path d="M11.297 9.176a3.5 3.5 0 0 0-4.474\
-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829l.822.822zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.\
823a2.5 2.5 0 0 0 2.829 2.829z"/><path d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 \
8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.\
029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 \
12-.708.708z"/>\
</svg>'
