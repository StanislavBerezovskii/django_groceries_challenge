import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# APPLICATION SETTINGS:

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DEBUG')
if DEBUG == 'True':
    DEBUG = True
else:
    DEBUG = False

DEBUG_DB = os.getenv('DEBUG_DB')
if DEBUG_DB == 'True':
    DEBUG_DB = True
else:
    DEBUG_DB = False


# DJANGO SETTINGS:

DATABASE_POSTGRES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('POSTGRES_DB', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='db'),
        'PORT': os.getenv('DB_PORT', default='5432'),
    }
}

DATABASE_SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = DATABASE_SQLITE if DEBUG_DB else DATABASE_POSTGRES

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    # Django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps:
    'drf_spectacular',
    'rest_framework',
    # Local apps:
    'api',
    'shop',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    "TITLE": "groceries API",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r'/api/',
}

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'


# INTERNATIONALIZATION SETTINGS:

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# MODEL SETTINGS:

ADMIN_PAGINATION = 15

CATEGORY_IMAGE_PATH: str = 'categories/'

NAME_MAX_LEN: int = 30

PRODUCT_IMAGE_PATH: str = 'products/'

SHOPPING_CART_MIN_QUANTITY: int = 1

SLUG_MAX_LEN: int = 30

SUBCATEGORY_IMAGE_PATH: str = 'subcategories/'


def set_category_image_name(instance, filename) -> str:
    """Creates category image name based on slug."""
    return f'{CATEGORY_IMAGE_PATH}{instance.slug}'


def set_product_image_name_l(instance, filename) -> str:
    """Creates product image name based on slug (large)."""
    return f'{PRODUCT_IMAGE_PATH}{instance.slug}_l'


def set_product_image_name_m(instance, filename) -> str:
    """Creates product image name based on slug (medium)."""
    return f'{PRODUCT_IMAGE_PATH}{instance.slug}_m'


def set_product_image_name_s(instance, filename) -> str:
    """Creates product image name based on slug (small)."""
    return f'{PRODUCT_IMAGE_PATH}{instance.slug}_s'


def set_subcategory_image_name(instance, filename) -> str:
    """Creates subcategory image name based on slug."""
    return f'{SUBCATEGORY_IMAGE_PATH}{instance.slug}'


# SECURITY SETTINGS:

ALLOWED_HOSTS = ['*', '80.87.108.66', 'localhost', 'web']

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECRET_KEY = os.getenv('SECRET_KEY')

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


# STATICS SETTINGS:

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

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
