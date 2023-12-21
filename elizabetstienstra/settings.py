"""
Django settings for elizabetstienstra project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['localhost', '8000-annakovesdi-elizabetsti-130ylo2gq63.ws-eu107.gitpod.io']
CSRF_TRUSTED_ORIGINS = []

EXTERNAL_HOSTNAME = os.getenv('EXTERNAL_HOSTNAME')

if EXTERNAL_HOSTNAME:
    SECRET_KEY = os.getenv('SECRET_KEY')
    EXTERNAL_CSRF = os.getenv('EXTERNAL_CSRF')
    HOST = os.getenv('HOST')
    ALLOWED_HOSTS.append(HOST)
    ALLOWED_HOSTS.append(EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(EXTERNAL_CSRF)
    STORAGE_DESTINATION = 's3'    

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    # sitemap
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # custom
    'home',
    'oeuvre',
    'about',
    'info',
    'cv',
    # allauth
    'allauth',
    'allauth.account',
    # packages
    'crispy_forms',
    'crispy_bootstrap4',
    'sweetify',
    'ckeditor',
    'storages',
    # csp
    'csp_helpers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# Security 

SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000 # work up to 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'

# CSP Securty Headers

CSP_DEFAULT_SRC = ["'self'", ]
CSP_STYLE_SRC = [
    "'self'", 
    "https://cdn.jsdelivr.net/", 
    "https://fonts.googleapis.com/", 
    "https://elisabetstienstra.s3.amazonaws.com/",
    "'unsafe-inline'",
]
CSP_SCRIPT_SRC = [
    "'self'", 
    # 'https://elizabetstienstra.com/',
]
CSP_INCLUDE_NONCE_IN = [
    'script-src',
]
CSP_CONNECT_SRC = [
    "'self'",
    "https://ka-f.fontawesome.com/",
    "http://*.cke-cs.com",
]
CSP_IMG_SRC = [
    "'self'", 
    'data:',
    'https://res.cloudinary.com/',
    "https://elisabetstienstra.s3.amazonaws.com/",
]
CSP_FRAME_SRC = ["'self'", ]
CSP_MEDIA_SRC = ["'self'", ]
CSP_MANIFEST_SRC = ["'self'", ]
CSP_FONT_SRC = [
    "'self'", 
    "https://fonts.gstatic.com/", 
    "https://fonts.googleapis.com/", 
    "https://ka-f.fontawesome.com/",
]

ROOT_URLCONF = 'elizabetstienstra.urls'

SITE_ID = 1

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WSGI_APPLICATION = 'elizabetstienstra.wsgi.application'

DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
DJANGO_SUPERUSER_USERNAME_FIELD = os.environ.get('DJANGO_SUPERUSER_USERNAME_FIELD', '')

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STORAGE_DESTINATION = os.environ.get('STORAGE_DESTINATION')
if STORAGE_DESTINATION == 's3':
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {
        'Access-Control-Allow-Origin': '*',
    }

    STATICFILES_DIRS = [
        'static',
    ]
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

    # public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = 'static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
