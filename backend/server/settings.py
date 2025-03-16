"""
Django settings for server project.
"""
import environ
import os

from datetime import timedelta

from pathlib import Path

import psycopg2

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

if not DEBUG:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_URL = 'https://api.plannder.com'
    CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
else:
    SECRET_KEY = 'LYLmGW3Eabxzn2kdQeFGumZflknV1aFQAlIamvbuAjw='
    API_URL = 'https://127.0.0.1:8000'

    CORS_ALLOWED_ORIGINS = [
        "https://localhost.com",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:9000",
        "https://127.0.0.1:8000",
    ]

    ALLOWED_HOSTS = [
        '0.0.0.0',
        '127.0.0.1',
        'localhost',
        'testserver',
    ]

# Application definition

INSTALLED_ADDITIONAL_APPS = [
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'sslserver',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
]

OWN_ADDITIONAL_APPS = [
    'dicts',
    'users',
    'permissions',
    'trips',
    'user_auth',
    'itineraries',
    'chats',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + INSTALLED_ADDITIONAL_APPS + OWN_ADDITIONAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'server.wsgi.application'

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis server URL
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Rest framework

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# JWT token

SIMPLE_JWT = {
    'BLACKLIST_AFTER_ROTATION': True,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Plannder API',
    'DESCRIPTION': 'Engineering thesis PJATK',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'DISABLE_DEFAULT_SCHEMA_GROUPING': True,
    'COMPONENT_SPLIT_REQUEST': True,
    'TAGS': [
        {'name': 'Trip', 'description': 'Endpoints for managing trips.'},
        {'name': 'Ticket', 'description': 'Endpoints for managing tickets.'},
        {'name': 'Budget', 'description': 'Endpoints for managing budgets.'},
        {'name': 'Expense', 'description': 'Endpoints for managing expenses.'},
        {'name': 'Itinerary', 'description': 'Endpoints for managing itineraries.'},
        {'name': 'Itinerary Activity', 'description': 'Endpoints for managing itinerary activities.'},
    ],
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Email config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

if not DEBUG:
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
else:
    EMAIL_HOST_USER = 'plannder@op.pl'
    EMAIL_HOST_PASSWORD = 'Pjatk12121212!'
    EMAIL_HOST = 'smtp.poczta.onet.pl'




# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = 'user_auth/login/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/graph_models/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "graph_models"),
]

MEDIA_URL = '' # TODO: ustawić
MEDIA_ROOT = '' # TODO: ustawić

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Database settings
CONN_MAX_AGE = 0

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
