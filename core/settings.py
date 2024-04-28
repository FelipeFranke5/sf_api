from pathlib import Path

from dotenv import dotenv_values


class EnvException(BaseException):
    pass


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ENV_FILE validation
ENV_FILE = dotenv_values(dotenv_path='.env')
DEBUG_MODE_ENV = ENV_FILE.get('DEBUG_MODE')
SECRET_KEY_ENV = ENV_FILE.get('DJANGO_SECRET_KEY')
ALLOWED_HOSTS_ENV = ENV_FILE.get('ALLOWED_HOSTS')

DB_NAME = ENV_FILE.get('POSTGRES_DB')
DB_USER = ENV_FILE.get('POSTGRES_USER')
DB_PASS = ENV_FILE.get('POSTGRES_PASSWORD')
DB_HOST = ENV_FILE.get('POSTGRES_HOST')
DB_PORT = ENV_FILE.get('POSTGRES_PORT')

MAIL_BE = ENV_FILE.get('EMAIL_BACKEND')
MAIL_HOST = ENV_FILE.get('EMAIL_HOST')
MAIL_HOST_USER = ENV_FILE.get('EMAIL_HOST_USER')
MAIL_HOST_PASS = ENV_FILE.get('EMAIL_HOST_PASSWORD')
MAIL_PORT = ENV_FILE.get('EMAIL_PORT')
MAIL_TLS = ENV_FILE.get('EMAIL_USE_TLS')
MAIL_SSL = ENV_FILE.get('EMAIL_USE_SSL')
MAIL_SECURE_ADD1 = ENV_FILE.get('EMAIL_SECURE_ADD1')

if not ENV_FILE:
    raise EnvException('Missing ENV_FILE.')

if not DEBUG_MODE_ENV:
    raise EnvException('Missing DEBUG_MODE_ENV.')

if not DEBUG_MODE_ENV in {'0', '1'}:
    raise EnvException('DEBUG_MODE_ENV should be "0" or "1".')

if not SECRET_KEY_ENV:
    raise EnvException('Missing SECRET_KEY_ENV.')

if not ALLOWED_HOSTS_ENV:
    raise EnvException('Missing ALLOWED_HOSTS.')

# Check for DB values in the ENV file
DB_VALIDATOR = [
    not DB_NAME,
    not DB_USER,
    not DB_PASS,
    not DB_PORT,
    not DB_HOST,
]
if any(DB_VALIDATOR):
    raise EnvException('Missing DB_*.')

# Check for MAIL values in the ENV file
MAIL_VALITADOR = [
    not MAIL_BE,
    not MAIL_HOST,
    not MAIL_HOST_USER,
    not MAIL_HOST_PASS,
    not MAIL_PORT,
    not MAIL_TLS,
    not MAIL_SECURE_ADD1,
    not MAIL_SSL,
    MAIL_TLS not in {'0', '1'},
    MAIL_SSL not in {'0', '1'},
    len([x for x in MAIL_PORT if x.isdigit()]) != len(MAIL_PORT),
]
if any(MAIL_VALITADOR):
    raise EnvException('Missing / wrong MAIL_*.')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

DEBUG = bool(int(DEBUG_MODE_ENV))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY_ENV

# SECURITY WARNING: don't run with debug turned on in production!

# Every host is allowed, if DEBUG is True
if DEBUG:
    ALLOWED_HOSTS = ['*']

# Manually set up the ALLOWED HOSTS, if DEBUG is False
ALLOWED_HOSTS = ALLOWED_HOSTS_ENV.split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-Party
    'rest_framework',
    'rest_framework_simplejwt',
    # My Apps
    'salesforce',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangorestframework_camel_case.middleware.CamelCaseMiddleWare',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Set up the STATIC_ROOT, pointing to PROD
STATIC_ROOT = BASE_DIR / 'prodstatic'

# Set up the STATIC_URL
STATIC_URL = 'static/'

# Set up the STATICFILES_DIRS
STATICFILES_DIRS = [
    BASE_DIR / 'mystatic'
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        'drf_excel.renderers.XLSXRenderer',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S',
}

# Set up the EMAIL configuration for use
EMAIL_BACKEND = MAIL_BE
EMAIL_HOST = MAIL_HOST
EMAIL_HOST_USER = MAIL_HOST_USER
EMAIL_HOST_PASSWORD = MAIL_HOST_PASS
EMAIL_PORT = int(MAIL_PORT)
EMAIL_USE_TLS = bool(int(MAIL_TLS))
EMAIL_USE_SSL = bool(int(MAIL_SSL))
EMAIL_SECURE_ADD1 = MAIL_SECURE_ADD1
